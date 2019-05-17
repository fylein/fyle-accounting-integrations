from django.apps import AppConfig
from django.conf import settings

from accounting_integrations.general.utils import perform_import


class ExportConfig(AppConfig):
    name = 'accounting_integrations.export'

    def ready(self):
        # Register the export drivers here
        from accounting_integrations.export.drivers import driver_registry

        for driver in settings.EXPORT_DRIVERS:
            driver_cls = perform_import(driver)
            driver_registry.register(driver_cls)
