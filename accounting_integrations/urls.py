"""accounting_integrations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from accounting_integrations.fyle_import import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('fyle-data/projects',
         login_required(views.ProjectListView.as_view()), name='project_list'),
    path('fyle-data/cost-centers',
         login_required(views.CostCenterListView.as_view()), name='costcenter_list'),
    path('fyle-data/categories',
         login_required(views.CategoryListView.as_view()), name='category_list'),
    path('fyle-data/employees',
         login_required(views.EmployeeListView.as_view()), name='employee_list'),
    path('fyle-data/expenses',
         login_required(views.ExpenseListView.as_view()), name='expense_list'),
    path('fyle-data/advances',
         login_required(views.AdvanceListView.as_view()), name='advance_list'),
    path('', login_required(views.IndexView.as_view()), name='index'),
]
