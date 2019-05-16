""" Utility functions for the Fyle App """
from allauth.socialaccount.models import SocialAccount
from datetime import datetime
from django.conf import settings
from fylesdk import FyleSDK

from accounting_integrations.fyle.models import (
    ImportBatch, Category, CostCenter, Employee, Expense)


def import_fyle_data(import_batch_id):
    """ Function for importing data from Fyle API """
    batch = ImportBatch.objects.get(pk=import_batch_id)
    social_account = SocialAccount.objects.get(user=batch.user)

    # Setup the fyle API
    fyle_api = FyleSDK(
        client_id=settings.FYLE_CLIENT_ID,
        client_secret=settings.FYLE_CLIENT_SECRET,
        refresh_token=social_account.socialtoken_set.first().token_secret
    )

    # Fetch the last updated date
    last_updated_at = datetime(2010, 1, 1)
    last_batch = ImportBatch.objects.filter().order_by('-created_at').first()
    if last_batch:
        last_updated_at = last_batch.created_at

    # Get the Project Data
    print(fyle_api.Projects.get())
    print(fyle_api.CostCenters.get())

    # Sync the Category Data
    for data in get_fyle_data(fyle_api.Categories, {}):
        defaults = {
            'name': data['name'],
            'code': data['code'],
            'fyle_category': data['fyle_category'],
            'sub_category': data['sub_category'],
            'enabled': data['enabled'],
        }
        Category.objects.update_or_create(
            id=data['id'], user=batch.user, defaults=defaults)

    for data in get_fyle_data(fyle_api.Employees, {}, False):
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
            id=data['id'], user=batch.user, defaults=defaults)

    expense_params = {
        'updated_at': 'gte:' + last_updated_at.strftime('%Y-%m-%dT%H:%M:%S.000Z')}
    for data in get_fyle_data(fyle_api.Expenses, expense_params, False):
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
            id=data['id'], user=batch.user, defaults=defaults)
        batch.expenses.add(expense)

    print(fyle_api.Advances.get())


def get_fyle_data(schema, params, paginated=False):
    """ Get the data from the Fyle API """
    data = []
    print(params)
    if not paginated:
        data.extend(schema.get(**params)['data'])

    else:
        offset = 0
        while True:
            params.update({
                'offset': offset,
                'limit': 100
            })
            cur_data = schema.get(**params)['data']
            if not cur_data:
                break
            else:
                data.extend(cur_data)
                offset = cur_data[-1]['id']

    return data
