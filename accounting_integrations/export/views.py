from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, View

from accounting_integrations.export.models import ExportSetting, ExportBatch
from accounting_integrations.export.forms import ExportSettingForm


class ExportSettingUpdateView(SuccessMessageMixin, UpdateView):
    """ View for managing the  general settings"""
    template_name = 'export/export_setting.html'
    model = ExportSetting
    form_class = ExportSettingForm
    success_url = reverse_lazy('export_setting')
    success_message = 'Export Settings have been updated successfully'

    def get_object(self, queryset=None):
        """ Return the fyle import configuration for the user"""
        export_setting, _ = self.get_queryset().\
            get_or_create(user=self.request.user)
        return export_setting
