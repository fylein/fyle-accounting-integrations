""" Utility functions for the Fyle App """
import json
from allauth.socialaccount.models import SocialAccount
from datetime import datetime
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils import dateparse
from fylesdk import FyleSDK

from accounting_integrations.fyle.models import (
    ImportBatch, Category, CostCenter, Employee, Expense, Project, Advance)
from accounting_integrations.general.models import File


class ImportBatchRunner:

    def __init__(self, import_batch_id):
        self.batch_id = import_batch_id
        self.batch = ImportBatch.objects.get(pk=self.batch_id)

        # Setup the fyle API
        social_account = SocialAccount.objects.get(user=self.batch.user)
        self.fyle_api = FyleSDK(
            client_id=settings.FYLE_CLIENT_ID,
            client_secret=settings.FYLE_CLIENT_SECRET,
            refresh_token=social_account.socialtoken_set.first().token_secret
        )

        self.batch.min_updated_at = None
        self.batch.max_updated_at = None

    def _update_min_max_updated_at(self, data):
        """ Function to get the Min and Max Updated At values"""
        if data.get('updated_at'):
            updated_at = dateparse.parse_datetime(data.get('updated_at'))
            if not self.batch.min_updated_at or \
                    updated_at < self.batch.min_updated_at:
                self.batch.min_updated_at = updated_at
            if not self.batch.max_updated_at or \
                    updated_at > self.batch.max_updated_at:
                self.batch.max_updated_at = updated_at

    def _get_fyle_data(self, schema, params, paginated=False):
        """ Get the data from the Fyle API """
        data = []
        if not paginated:
            data.extend(schema.get(**params)['data'])

        else:
            limit = 100
            page = 1
            while True:
                params.update({
                    'offset': (page - 1) * limit,
                    'limit': limit
                })
                cur_data = schema.get(**params)['data']
                data.extend(cur_data)
                if len(cur_data) < limit:
                    break
                else:
                    page += 1

        # Save the data to the batch
        if data:
            data_file = File(type='application/json', related_object=self.batch)

            data_file.contents.save(
                f'fyle_{schema.__class__.__name__.lower()}_'
                f'data_{self.batch.id}.json',
                ContentFile(json.dumps(data, indent=4).encode('utf-8')))
        return data

    def _import_project_data(self):
        """ Import the Project Data """
        for data in self._get_fyle_data(
                self.fyle_api.Projects, {'active_only': False}):
            defaults = {
                'name': data['name'],
                'description': data['description'],
                'active': data['active'],
            }
            Project.objects.update_or_create(
                id=data['id'], user=self.batch.user, defaults=defaults)

    def _import_costcenter_data(self):
        """ Import the Cost Center Data """
        for data in self._get_fyle_data(
                self.fyle_api.CostCenters, {'active_only': False}):
            self._update_min_max_updated_at(data)
            defaults = {
                'name': data['name'],
                'description': data['description'],
            }
            CostCenter.objects.update_or_create(
                id=data['id'], user=self.batch.user, defaults=defaults)

    def _import_category_data(self):
        """ Import the Category Data """
        for data in self._get_fyle_data(
                self.fyle_api.Categories, {'active_only': False}):
            self._update_min_max_updated_at(data)
            defaults = {
                'name': data['name'],
                'code': data['code'],
                'fyle_category': data['fyle_category'],
                'sub_category': data['sub_category'],
                'enabled': data['enabled'],
            }
            Category.objects.update_or_create(
                id=data['id'], user=self.batch.user, defaults=defaults)

    def _import_employee_data(self):
        """ Import the Employee Data """
        for data in self._get_fyle_data(self.fyle_api.Employees, {}, True):
            self._update_min_max_updated_at(data)
            defaults = {
                'employee_email': data['employee_email'],
                'employee_code': data['employee_code'],
                'full_name': data['full_name'],
                'location': data['location'],
                'level': data['level'],
                'business_unit': data['business_unit'],
                'department': data['department'],
                'sub_department': data['sub_department'],
                'disabled': data['disabled'],
                'org_id': data['org_id'],
                'org_name': data['org_name'],
            }
            if data['default_cost_center_name']:
                defaults['default_cost_center'] = CostCenter.objects.filter(
                    name=data['default_cost_center_name']).first()
            Employee.objects.update_or_create(
                id=data['id'], user=self.batch.user, defaults=defaults)

    def _import_expense_data(self, last_updated_at):
        """ Import the Expense Data """
        expense_params = {
            'updated_at':
                'gte:' + last_updated_at.strftime('%Y-%m-%dT%H:%M:%S.000Z')}
        for data in self._get_fyle_data(
                self.fyle_api.Expenses, expense_params, True):
            self._update_min_max_updated_at(data)

            defaults = {
                'currency': data['currency'],
                'amount': data['amount'],
                'foreign_currency': data['foreign_currency'],
                'foreign_amount': data['foreign_amount'],
                'purpose': data['purpose'],
                'custom_properties': data['custom_properties'],
                'reimbursable': data['reimbursable'],
                'state': data['state'],
                'spent_at': data['spent_at'],
                'created_at': data['created_at'],
                'approved_at': data['approved_at'],
                'verified': data['verified'],
                'verified_at': data['verified_at'],
                'reimbursed_at': data['reimbursed_at'],
                'vendor': data['vendor'],
            }
            if data['employee_id']:
                defaults['employee'] = Employee.objects.filter(
                    id=data['employee_id']).first()
            if data['project_id']:
                defaults['project'] = Project.objects.filter(
                    id=data['project_id']).first()
            if data['cost_center_id']:
                defaults['cost_center'] = CostCenter.objects.filter(
                    id=data['cost_center_id']).first()
            if data['category_id']:
                defaults['category'] = Category.objects.filter(
                    id=data['category_id']).first()

            expense, _ = Expense.objects.update_or_create(
                id=data['id'], user=self.batch.user, defaults=defaults)
            self.batch.expenses.add(expense)

    def _import_advance_data(self, last_updated_at):
        """ Import the Advance Data """
        advance_params = {
            'updated_at':
                'gte:' + last_updated_at.strftime('%Y-%m-%dT%H:%M:%S.000Z')}
        for data in self._get_fyle_data(
                self.fyle_api.Advances, advance_params, True):
            self._update_min_max_updated_at(data)
            defaults = {
                'currency': data['currency'],
                'amount': data['amount'],
                'original_currency': data['original_currency'],
                'original_amount': data['original_amount'],
                'purpose': data['purpose'],
                'issued_at': data['issued_at'],
                'payment_mode': data['payment_mode'],
                'reference': data['reference'],
            }
            if data['employee_id']:
                defaults['employee'] = Employee.objects.filter(
                    id=data['employee_id']).first()
            if data['project_id']:
                defaults['project'] = Project.objects.filter(
                    id=data['project_id']).first()
            advance, _ = Advance.objects.update_or_create(
                id=data['id'], user=self.batch.user, defaults=defaults)
            self.batch.advances.add(advance)

    def import_fyle_data(self):
        """ Function for importing data from Fyle API """

        # Fetch the last updated date
        last_updated_at = datetime(2010, 1, 1)
        last_batch = ImportBatch.objects.exclude(id=self.batch.id).\
            order_by('-created_at').first()
        if last_batch:
            last_updated_at = last_batch.created_at

        # Import the Project Data
        self._import_project_data()

        # Import the Cost Center Data
        self._import_costcenter_data()

        # Import the Category Data
        self._import_category_data()

        # Import the Employee Data
        self._import_employee_data()

        # Import the Expense Data
        self._import_expense_data(last_updated_at)

        # Import the Advance Data
        self._import_advance_data(last_updated_at)

        self.batch.status = 'C'
        self.batch.save()

