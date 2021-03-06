from django.apps import apps
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, View, ListView

from accounting_integrations.general.models import File
from accounting_integrations.fyle.models import ImportBatch
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


class ExportBatchListView(ListView):
    """ View for listing of Import Batches """
    template_name = 'export/exportbatch_list.html'
    model = ExportBatch
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        """ Show only current user data """
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user).\
            select_related('import_batch')
        return queryset


class ExportBatchPrepareView(View):
    """ Run the export prepare for all pending import batches """

    def post(self, request):
        """ Show only current user data """
        # Check if the export driver has been setup
        setting = ExportSetting.objects.filter(user=request.user).first()
        if not setting or not setting.driver:
            messages.warning(
                self.request, 'You need to setup the export driver '
                              'before running exports.')
            return HttpResponseRedirect(reverse_lazy('export_setting'))

        export_app = apps.get_app_config('export')
        driver_cls = export_app.get_driver(setting.driver)

        # Get the list of pending imports
        pending_imports = ImportBatch.objects.\
            filter(exportbatch=None, status='C').\
            order_by('-created_at')
        for batch in pending_imports:
            export = ExportBatch.objects.create(
                import_batch=batch, user=request.user)
            driver = driver_cls(export.id)
            driver.prepare()
            export.status = 'PR'
            export.save()

        messages.success(
            self.request, 'Export batches created for all pending Imports')

        return HttpResponseRedirect(reverse_lazy('exportbatch_list'))


class ExportBatchFileListView(ListView):
    """ View for listing of Files of the Export Batch """
    template_name = 'general/file_list.html'
    model = File
    paginate_by = 10

    def get_queryset(self):
        """ Show only current user data """
        queryset = ExportBatch.objects.get(
            id=self.kwargs.get('pk')).files.order_by('id')
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['exportbatch_id'] = self.kwargs.get('pk')
        return context_data


class ExportBatchPushView(View):
    """ Run the export prepare for all pending import batches """

    def post(self, request, pk):
        """ Show only current user data """
        # Check if the export driver has been setup
        setting = ExportSetting.objects.filter(user=request.user).first()
        if not setting or not setting.driver:
            messages.warning(
                self.request, 'You need to setup the export driver '
                              'before running exports.')
            return HttpResponseRedirect(reverse_lazy('export_setting'))

        # Get the driver class for this user
        export_app = apps.get_app_config('export')
        driver_cls = export_app.get_driver(setting.driver)

        # Get the export batch object
        export_batch = ExportBatch.objects.get(pk=pk)

        # Push the export batch and update its status.
        driver = driver_cls(export_batch.id)
        driver.push()
        export_batch.status = 'PU'
        export_batch.save()

        messages.success(self.request,
                         f'Export batch {pk} has been pushed successfully.')

        return HttpResponseRedirect(reverse_lazy('exportbatch_list'))
