""" Define generic reusable decorators here """
import csv
import io
from django.utils.text import slugify
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage

from accounting_integrations.export.drivers.base import BaseExportDriver
from accounting_integrations.general.models import File, GeneralSetting
from accounting_integrations.fyle.models import (
    Project, CostCenter, Category, Employee, Expense, Advance)


class GenericCsvExportDriver(BaseExportDriver):
    """ A Generic Drive for Exporting to CSV """
    name = 'Generic CSV Driver'

    # Define the column mappings for each Fyle entity, the mapping must be a
    # list of tuples with source column and destination column
    column_mappings = {
        'Project': [],
        'CostCenter': [],
        'Category': [],
        'Employee': [],
        'Expense': [],
        'Advance': []
    }

    def _save_prepared_data(self, model_name, items):
        # Generate the CSV file using the mappings
        column_map = self.column_mappings.get(model_name)
        if items and column_map:
            output = io.StringIO()
            output_csv = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)

            # Get the columns for the CSV
            dest_col = [x for _, x in column_map]
            source_col = {y: x for x, y in column_map}
            output_csv.writerow(dest_col)

            for obj in items:
                row = []
                for col in dest_col:
                    row.append(getattr(obj, source_col[col], None))
                output_csv.writerow(row)

            # Save the CSV to a file and append it
            data_file = File(type='text/csv', related_object=self.export_batch)
            data_file.contents.save(
                f'{slugify(self.name)}_{model_name}_'
                f'data_{self.export_batch.id}.csv',
                ContentFile(output.getvalue().encode('utf-8')))

    def prepare(self):
        """ Prepare the Export CSV Data from the Import JSON Files """
        # Load the project, cost-center, category and employee data
        for model in [Project, CostCenter, Category, Employee]:
            self._save_prepared_data(model.__name__, model.objects.all())

        # Load the rest of the models
        for model in [Expense, Advance]:
            self._save_prepared_data(
                model.__name__,
                model.objects.filter(importbatch=self.export_batch.import_batch))

    def push(self):
        """ Email the prepared CSV data to the User """
        # Get the general settings for the user
        setting = GeneralSetting.objects.get(user=self.export_batch.user)
        if not setting.notification_emails:
            return

        email_message = EmailMessage(
            subject=f'Results of export batch process {self.export_batch.id}',
            body=f'Please find attached the files exported from the import batch '
                 f'process {self.export_batch.import_batch.id} executed on '
                 f'{self.export_batch.import_batch.created_at}.',
            to=setting.notification_emails.split(',')
        )

        # Attach the exported files
        for file in self.export_batch.files.all():
            email_message.attach(
                file.filename, file.contents.read(), file.type)

        # Send the mail message
        email_message.send()
