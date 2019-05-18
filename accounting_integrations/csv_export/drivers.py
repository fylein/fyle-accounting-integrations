from accounting_integrations.export.drivers.generic import GenericCsvExportDriver


class SampleCsvExportDriver(GenericCsvExportDriver):
    """ A sample implementation of the CSV Export Driver """

    name = 'Sample CSV Exporter'

    column_mappings = {
        'projects': [('id', 'ID'), ('name', 'Name'),
                     ('description', 'Description')],
        'costcenters': [('id', 'ID'), ('name', 'Name'),
                        ('description', 'Description')],
        'categories': [('id', 'ID'), ('name', 'Name'), ('code', 'Code'),
                       ('fyle_category', 'Fyle Category'),
                       ('sub_category', 'Sub Category')],
        'employees': [('id', 'ID'), ('employee_email', 'Employee Email'),
                      ('employee_code', 'Employee Code'),
                      ('level', 'Level'), ('department', 'Department'),
                      ('sub_department', 'Sub Department')],
        'expenses': [('id', 'ID'), ('employee_id', 'Employee ID'),
                     ('currency', 'Currency'), ('amount', 'Amount'),
                     ('purpose', 'Purpose'), ('state', 'State'),
                     ('created_at', 'Created At'), ('approved_at', 'Approved At'),
                     ('verified', 'Verified'), ('verified_at', 'Verified At')],
        'advances': [('id', 'ID'), ('employee_id', 'Employee ID'),
                     ('currency', 'Currency'), ('amount', 'Amount'),
                     ('purpose', 'Purpose'), ('issued_at', 'Issued At'),
                     ('reference', 'Reference')],
    }
