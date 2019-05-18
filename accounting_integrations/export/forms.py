from django import forms
from django.apps import apps

from accounting_integrations.export.models import ExportSetting


class ExportSettingForm(forms.ModelForm):
    driver = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        export_app = apps.get_app_config('export')
        self.fields['driver'].choices = export_app.get_driver_list()

    class Meta:
        model = ExportSetting
        fields = ['driver',]
