from accounting_integrations.export.drivers.generic import GenericCsvExportDriver


class SampleCsvExportDriver(GenericCsvExportDriver):
    """ A sample implementation of the CSV Export Driver """

    name = 'Sample CSV Exporter'

    column_mappings = {
        'Project': [('id', 'ID'), ('name', 'Name'),
                    ('description', 'Description')],
        'CostCenter': [('id', 'ID'), ('name', 'Name'),
                       ('description', 'Description')],
        'Category': [('id', 'ID'), ('name', 'Name'), ('code', 'Code'),
                     ('fyle_category', 'Fyle Category'),
                     ('sub_category', 'Sub Category')],
        'Employee': [('id', 'ID'), ('employee_email', 'Employee Email'),
                     ('employee_code', 'Employee Code'),
                     ('level', 'Level'), ('department', 'Department'),
                     ('sub_department', 'Sub Department')],
        'Expense': [('id', 'ID'), ('employee_id', 'Employee ID'),
                    ('currency', 'Currency'), ('amount', 'Amount'),
                    ('purpose', 'Purpose'), ('state', 'State'),
                    ('created_at', 'Created At'), ('approved_at', 'Approved At'),
                    ('verified', 'Verified'), ('verified_at', 'Verified At')],
        'Advance': [('id', 'ID'), ('employee_id', 'Employee ID'),
                    ('currency', 'Currency'), ('amount', 'Amount'),
                    ('purpose', 'Purpose'), ('issued_at', 'Issued At'),
                    ('reference', 'Reference')],
    }
