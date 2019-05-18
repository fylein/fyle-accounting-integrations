from django.apps import AppConfig
from django.conf import settings

from accounting_integrations.general.utils import perform_import


class ExportConfig(AppConfig):
    name = 'accounting_integrations.export'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._driver_registry = {}

    def register_driver(self, driver_cls):
        driver_name = '.'.join([driver_cls.__module__, driver_cls.__qualname__])
        if not self._driver_registry.get(driver_name):
            self._driver_registry[driver_name] = driver_cls

    def get_driver(self, driver_name):
        """Retrieve Driver class registered by `driver_name`"""
        try:
            return self._driver_registry[driver_name]
        except KeyError:
            raise AssertionError(f'No driver registered with name "{driver_name}"')

    def get_driver_list(self):
        """Return a list of registered Driver key and names """
        return [(dn, dc.name) for dn, dc in self._driver_registry.items()]

    def ready(self):
        # Register the export drivers here
        for driver in settings.EXPORT_DRIVERS:
            driver_cls = perform_import(driver)
            self.register_driver(driver_cls)
