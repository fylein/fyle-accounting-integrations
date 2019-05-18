from django.urls import path
from django.contrib.auth.decorators import login_required

from accounting_integrations.export import views

urlpatterns = [
    path('export-settings',
         login_required(views.ExportSettingUpdateView.as_view()),
         name='export_setting'),
    path('export-batches',
         login_required(views.ExportBatchListView.as_view()),
         name='exportbatch_list'),
    path('export-batches/create',
         login_required(views.ExportBatchCreateView.as_view()),
         name='exportbatch_create'),
    path('export-batches/<int:pk>/files',
         login_required(views.ExportBatchFileListView.as_view()),
         name='exportbatch_files'),
]
