from django.urls import path
from django.contrib.auth.decorators import login_required

from accounting_integrations.export import views

urlpatterns = [
    path('settings',
         login_required(views.ExportSettingUpdateView.as_view()),
         name='export_setting'),
]
