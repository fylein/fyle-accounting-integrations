from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView, View

from accounting_integrations.general.models import GeneralSetting, File


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


class DownloadFileView(View):
    """ View for downloading a file  """

    def get(self, request, pk, *args, **kwargs):
        file_obj = File.objects.get(pk=pk)
        response = HttpResponse(content_type=file_obj.type)
        disposition_type = 'attachment'
        response['Content-Disposition'] = \
            disposition_type + '; filename=' + file_obj.filename
        response.write(file_obj.contents.read())
        return response

