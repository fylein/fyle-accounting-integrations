from django.urls import path
from django.contrib.auth.decorators import login_required
from accounting_integrations.fyle import views

urlpatterns = [
    path('projects',
         login_required(views.ProjectListView.as_view()), name='project_list'),
    path('projects/<str:pk>/update',
         login_required(views.ProjectUpdateView.as_view()), name='project_update'),
    path('cost-centers',
         login_required(views.CostCenterListView.as_view()), name='costcenter_list'),
    path('cost-centers/<str:pk>/update',
         login_required(views.CostCenterUpdateView.as_view()), name='costcenter_update'),
    path('categories',
         login_required(views.CategoryListView.as_view()), name='category_list'),
    path('categories/<int:pk>/update',
         login_required(views.CategoryUpdateView.as_view()), name='category_update'),
    path('employees',
         login_required(views.EmployeeListView.as_view()), name='employee_list'),
    path('employees/<str:pk>/update',
         login_required(views.EmployeeUpdateView.as_view()), name='employee_update'),
    path('expenses',
         login_required(views.ExpenseListView.as_view()), name='expense_list'),
    path('expenses/<str:pk>',
         login_required(views.ExpenseDetailView.as_view()), name='expense_detail'),
    path('advances/<str:pk>',
         login_required(views.AdvanceDetailView.as_view()), name='advance_detail'),
    path('advances',
         login_required(views.AdvanceListView.as_view()), name='advance_list')

]