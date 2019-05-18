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
    path('export-batches/prepare',
         login_required(views.ExportBatchPrepareView.as_view()),
         name='exportbatch_prepare'),
    path('export-batches/<int:pk>/files',
         login_required(views.ExportBatchFileListView.as_view()),
         name='exportbatch_files'),
    path('export-batches/<int:pk>/push',
         login_required(views.ExportBatchPushView.as_view()),
         name='exportbatch_push'),
]
