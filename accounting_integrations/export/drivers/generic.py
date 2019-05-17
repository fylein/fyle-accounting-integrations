""" Define generic reusable decorators here """
import csv
import json
import io
from django.utils.text import slugify
from django.core.files.base import ContentFile

from accounting_integrations.export.drivers.base import BaseExportDriver
from accounting_integrations.general.models import File


class GenericCsvExportDriver(BaseExportDriver):
    """ A Generic Drive for Exporting to CSV """
    name = 'Generic CSV Driver'
    column_mappings = {
        'projects': {},
        'costcenters': {},
        'categories': {},
        'employees': {},
        'expenses': {},
        'advances': {}
    }

    def prepare(self):
        """ Prepare the Export CSV Data from the Import JSON Files """
        for file in self.export_batch.import_batch.files:
            data_type = file.filename.split('_')[1]

            # Generate the CSV file using the mappings
            column_map = self.column_mappings.get(data_type)
            if column_map:
                import_data = json.loads(file.contents.read())
                output = io.BytesIO()
                output_csv = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)

                # Get the columns for the CSV
                columns = column_map.items()
                output_csv.writerow(columns)
                for data in import_data:
                    row = []
                    for col in columns:
                        row.append(data.get(col))
                    output_csv.writerow(row)

                # Save the CSV to a file and append it
                data_file = File(type='text/csv', related_object=self.export_batch)
                data_file.contents.save(
                    f'{slugify(self.name)}_{data_type}_'
                    f'data_{self.export_batch.id}.csv',
                    ContentFile(output.getvalue()))

    def push(self):
        """ Email the prepared CSV data to the User """
