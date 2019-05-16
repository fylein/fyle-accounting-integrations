from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy

from accounting_integrations.general.models import GeneralSetting


class GeneralSettingUpdateView(SuccessMessageMixin, UpdateView):
    """ View for managing the  general settings"""
    template_name = 'general/general_setting.html'
    model = GeneralSetting
    fields = ['notification_emails']
    success_url = reverse_lazy('general_setting')
    success_message = 'General Settings have been updated successfully'

    def get_object(self, queryset=None):
        """ Return the fyle import configuration for the user"""
        import_config, _ = self.get_queryset().get_or_create(user=self.request.user)
        return import_config
