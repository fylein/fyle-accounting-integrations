from django.urls import path
from django.contrib.auth.decorators import login_required
from accounting_integrations.fyle_import import views

urlpatterns = [
    path('fyle-data/projects',
         login_required(views.ProjectListView.as_view()), name='project_list'),
    path('fyle-data/projects/<str:pk>/update',
         login_required(views.ProjectUpdateView.as_view()), name='project_update'),
    path('fyle-data/cost-centers',
         login_required(views.CostCenterListView.as_view()), name='costcenter_list'),
    path('fyle-data/cost-centers/<str:pk>/update',
         login_required(views.CostCenterUpdateView.as_view()), name='costcenter_update'),
    path('fyle-data/categories',
         login_required(views.CategoryListView.as_view()), name='category_list'),
    path('fyle-data/categories/<int:pk>/update',
         login_required(views.CategoryUpdateView.as_view()), name='category_update'),
    path('fyle-data/employees',
         login_required(views.EmployeeListView.as_view()), name='employee_list'),
    path('fyle-data/employees/<str:pk>/update',
         login_required(views.EmployeeUpdateView.as_view()), name='employee_update'),
    path('fyle-data/expenses',
         login_required(views.ExpenseListView.as_view()), name='expense_list'),
    path('fyle-data/expenses/<str:pk>',
         login_required(views.ExpenseDetailView.as_view()), name='expense_detail'),
    path('fyle-data/advances/<str:pk>',
         login_required(views.AdvanceDetailView.as_view()), name='advance_detail'),
    path('fyle-data/advances',
         login_required(views.AdvanceListView.as_view()), name='advance_list'),
    path('dashboard', login_required(views.IndexView.as_view()), name='index'),

]
