from django.urls import path
from django.contrib.auth.decorators import login_required
from accounting_integrations.general import views

urlpatterns = [
    path('settings',
         login_required(views.GeneralSettingUpdateView.as_view()), name='general_setting'),
    path('files/<int:pk>',
         login_required(views.DownloadFileView.as_view()), name='download_file'),
]
