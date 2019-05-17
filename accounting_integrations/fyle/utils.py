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

    def import_fyle_data(self):
        """ Function for importing data from Fyle API """
        social_account = SocialAccount.objects.get(user=self.batch.user)

        # Setup the fyle API
        fyle_api = FyleSDK(
            client_id=settings.FYLE_CLIENT_ID,
            client_secret=settings.FYLE_CLIENT_SECRET,
            refresh_token=social_account.socialtoken_set.first().token_secret
        )

        # Fetch the last updated date
        last_updated_at = datetime(2010, 1, 1)
        last_batch = ImportBatch.objects.exclude(id=self.batch.id).\
            order_by('-created_at').first()
        if last_batch:
            last_updated_at = last_batch.created_at
        min_updated_at, max_updated_at = None, None

        # Sync the Project Data
        for data in self.get_fyle_data(fyle_api.Projects, {}):
            min_updated_at, max_updated_at = self.get_min_max_updated_at(
                data, min_updated_at, max_updated_at)
            defaults = {
                'name': data['name'],
                'description': data['description'],
                'active': data['active'],
            }
            Project.objects.update_or_create(
                id=data['id'], user=self.batch.user, defaults=defaults)

        # Sync the Cost Center Data
        for data in self.get_fyle_data(fyle_api.CostCenters, {}):
            min_updated_at, max_updated_at = self.get_min_max_updated_at(
                data, min_updated_at, max_updated_at)
            defaults = {
                'name': data['name'],
                'description': data['description'],
            }
            CostCenter.objects.update_or_create(
                id=data['id'], user=self.batch.user, defaults=defaults)

        # Sync the Category Data
        for data in self.get_fyle_data(fyle_api.Categories, {}):
            min_updated_at, max_updated_at = self.get_min_max_updated_at(
                data, min_updated_at, max_updated_at)
            defaults = {
                'name': data['name'],
                'code': data['code'],
                'fyle_category': data['fyle_category'],
                'sub_category': data['sub_category'],
                'enabled': data['enabled'],
            }
            Category.objects.update_or_create(
                id=data['id'], user=self.batch.user, defaults=defaults)

        for data in self.get_fyle_data(fyle_api.Employees, {}, True):
            min_updated_at, max_updated_at = self.get_min_max_updated_at(
                data, min_updated_at, max_updated_at)
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

        expense_params = {
            'updated_at': 'gte:' + last_updated_at.strftime('%Y-%m-%dT%H:%M:%S.000Z')}
        for data in self.get_fyle_data(fyle_api.Expenses, expense_params, True):
            min_updated_at, max_updated_at = self.get_min_max_updated_at(
                data, min_updated_at, max_updated_at)
            defaults = {
                'employee_id': data['employee_id'],
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
                'project_id': data['project_id'],
                'cost_center_id': data['cost_center_id'],
                'category_id': data['category_id'],
            }
            expense, _ = Expense.objects.update_or_create(
                id=data['id'], user=self.batch.user, defaults=defaults)
            self.batch.expenses.add(expense)

        advance_params = {
            'updated_at': 'gte:' + last_updated_at.strftime('%Y-%m-%dT%H:%M:%S.000Z')}
        for data in self.get_fyle_data(fyle_api.Advances, advance_params, True):
            min_updated_at, max_updated_at = self.get_min_max_updated_at(
                data, min_updated_at, max_updated_at)
            defaults = {
                'employee_id': data['employee_id'],
                'currency': data['currency'],
                'amount': data['amount'],
                'original_currency': data['original_currency'],
                'original_amount': data['original_amount'],
                'purpose': data['purpose'],
                'issued_at': data['issued_at'],
                'payment_mode': data['payment_mode'],
                'reference': data['reference'],
                'project_id': data['project_id'],
            }
            advance, _ = Advance.objects.update_or_create(
                id=data['id'], user=self.batch.user, defaults=defaults)
            self.batch.advances.add(advance)

        self.batch.min_updated_at = min_updated_at
        self.batch.max_updated_at = max_updated_at
        self.batch.save()

    def get_fyle_data(self, schema, params, paginated=False):
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
        data_file = File(type='application/json', related_object=self.batch)

        data_file.contents.save(
            f'fyle_{schema.__class__.__name__.lower()}_data_{self.batch.id}.json',
            ContentFile(json.dumps(data).encode('utf-8')))
        return data

    @staticmethod
    def get_min_max_updated_at(data, min_updated_at, max_updated_at):
        """ Function to get the Min and Max Updated At values"""
        if data.get('updated_at'):
            updated_at = dateparse.parse_datetime(data.get('updated_at'))
            if not min_updated_at or updated_at < min_updated_at:
                min_updated_at = updated_at
            if not max_updated_at or updated_at > max_updated_at:
                max_updated_at = updated_at

        return min_updated_at, max_updated_at
