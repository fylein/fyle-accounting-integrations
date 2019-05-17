from django import forms

from accounting_integrations.export.models import ExportSetting
from accounting_integrations.export.drivers import driver_registry


class ExportSettingForm(forms.ModelForm):
    driver = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['driver'].choices = driver_registry.get_driver_list()

    class Meta:
        model = ExportSetting
        fields = ['driver',]
