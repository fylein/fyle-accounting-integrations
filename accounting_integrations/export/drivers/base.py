""" Define the Base Interface for the Export Driver """
from abc import ABCMeta, abstractmethod

from accounting_integrations.general.utils import singleton


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


@singleton
class DriverRegistry:
    """ A singleton class for maintaining the Driver Registry """
    def __init__(self):
        self._registry = {}

    def register(self, driver_cls):
        driver_name = '.'.join([driver_cls.__module__, driver_cls.__qualname__])
        if not self._registry.get(driver_name):
            self._registry[driver_name] = driver_cls

    def get_driver(self, driver_name):
        """Retrieve Driver class registered by `driver_name`"""
        try:
            return self._registry[driver_name]
        except KeyError:
            raise AssertionError(f'No driver registered with name "{driver_name}"')

    def get_driver_list(self):
        """Return a list of registered Driver key and names """
        return [(dn, dc.name) for dn, dc in self._registry.items()]


# Singleton Registry, populated with the help of @<register_driver> decorators
driver_registry = DriverRegistry()
