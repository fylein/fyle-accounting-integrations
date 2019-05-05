from django.views.generic import TemplateView, ListView

from accounting_integrations.fyle_import.models import (
    Project, CostCenter, Category, Employee, Expense, Advance)


class IndexView(TemplateView):
    template_name = 'index.html'


class ProjectListView(ListView):
    """ View for listing of Projects """
    template_name = 'project_list.html'
    model = Project
    paginate_by = 10
    ordering = ['name']

    def get_queryset(self):
        """ Show only current user data """
        queryset = super().get_queryset()
        queryset.filter(user=self.request.user)
        return queryset


class CostCenterListView(ListView):
    """ View for listing of Cost Centers """
    template_name = 'costcenter_list.html'
    model = CostCenter
    paginate_by = 10
    ordering = ['name']

    def get_queryset(self):
        """ Show only current user data """
        queryset = super().get_queryset()
        queryset.filter(user=self.request.user)
        return queryset


class CategoryListView(ListView):
    """ View for listing of Categories """
    template_name = 'category_list.html'
    model = Category
    paginate_by = 10
    ordering = ['name']

    def get_queryset(self):
        """ Show only current user data """
        queryset = super().get_queryset()
        queryset.filter(user=self.request.user)
        return queryset


class EmployeeListView(ListView):
    """ View for listing of Employees """
    template_name = 'employee_list.html'
    model = Employee
    paginate_by = 10
    ordering = ['full_name']

    def get_queryset(self):
        """ Show only current user data """
        queryset = super().get_queryset()
        queryset.filter(user=self.request.user)
        return queryset


class ExpenseListView(ListView):
    """ View for listing of Expenses """
    template_name = 'expense_list.html'
    model = Expense
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        """ Show only current user data """
        queryset = super().get_queryset()
        queryset.filter(user=self.request.user).select_related('employee')
        return queryset


class AdvanceListView(ListView):
    """ View for listing of advances """
    template_name = 'advance_list.html'
    model = Advance
    paginate_by = 10
    ordering = ['-issued_at']

    def get_queryset(self):
        """ Show only current user data """
        queryset = super().get_queryset()
        queryset.filter(user=self.request.user).\
            select_related('employee').select_related('project')
        return queryset
