""" Define the Base Interface for the Export Driver """
from abc import ABCMeta, abstractmethod


class BaseExportDriver(metaclass=ABCMeta):
    """ Base class for the Export Driver """
    name = ''

    def __init__(self, export_batch_id):
        from accounting_integrations.export.models import ExportBatch
        self.export_batch = ExportBatch.objects.get(pk=export_batch_id)

    @abstractmethod
    def prepare(self):
        """
        Abstract method to prepare the data from Fyle Imports.
        All Child classes must implement this method.
        """
        pass

    @abstractmethod
    def push(self):
        """
        Abstract method to push the prepared data to the destination.
        All Child classes must implement this method.
        """
        pass
