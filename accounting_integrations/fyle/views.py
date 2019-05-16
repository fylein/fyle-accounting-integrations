from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, ListView, UpdateView, DetailView
from django.urls import reverse_lazy

from accounting_integrations.fyle.models import (
    Project, CostCenter, Category, Employee, Expense, Advance, ImportBatch)


class IndexView(TemplateView):
    template_name = 'fyle/index.html'

    def get_context_data(self, **kwargs):
        """ Update the context for this view """
        context = super().get_context_data(**kwargs)
        context['recent_imports'] = ImportBatch.objects.\
            filter(user=self.request.user).\
            prefetch_related('expenses').prefetch_related('advances').\
            order_by('-created_at')[:5]
        return context


class ProjectListView(ListView):
    """ View for listing of Projects """
    template_name = 'fyle/project_list.html'
    model = Project
    paginate_by = 10
    ordering = ['name']

    def get_queryset(self):
        """ Show only current user data """
        queryset = super().get_queryset()
        queryset.filter(user=self.request.user)
        return queryset


class ProjectUpdateView(SuccessMessageMixin, UpdateView):
    """ View for updating a project """
    template_name = 'fyle/project_form.html'
    model = Project
    fields = ['code1', 'code2', 'code3']
    success_url = reverse_lazy('project_list')
    success_message = 'Project <strong>%(name)s</strong> has been ' \
                      'updated successfully'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )


class CostCenterListView(ListView):
    """ View for listing of Cost Centers """
    template_name = 'fyle/costcenter_list.html'
    model = CostCenter
    paginate_by = 10
    ordering = ['name']

    def get_queryset(self):
        """ Show only current user data """
        queryset = super().get_queryset()
        queryset.filter(user=self.request.user)
        return queryset


class CostCenterUpdateView(SuccessMessageMixin, UpdateView):
    """ View for updating a cost center """
    template_name = 'fyle/costcenter_form.html'
    model = CostCenter
    fields = ['code1', 'code2', 'code3']
    success_url = reverse_lazy('costcenter_list')
    success_message = 'Cost Center <strong>%(name)s</strong> has been ' \
                      'updated successfully'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )


class CategoryListView(ListView):
    """ View for listing of Categories """
    template_name = 'fyle/category_list.html'
    model = Category
    paginate_by = 10
    ordering = ['name']

    def get_queryset(self):
        """ Show only current user data """
        queryset = super().get_queryset()
        queryset.filter(user=self.request.user)
        return queryset


class CategoryUpdateView(SuccessMessageMixin, UpdateView):
    """ View for updating a category """
    template_name = 'fyle/category_form.html'
    model = Category
    fields = ['code1', 'code2', 'code3']
    success_url = reverse_lazy('category_list')
    success_message = 'Category <strong>%(name)s</strong> has been ' \
                      'updated successfully'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )


class EmployeeListView(ListView):
    """ View for listing of Employees """
    template_name = 'fyle/employee_list.html'
    model = Employee
    paginate_by = 10
    ordering = ['full_name']

    def get_queryset(self):
        """ Show only current user data """
        queryset = super().get_queryset()
        queryset.filter(user=self.request.user)
        return queryset


class EmployeeUpdateView(SuccessMessageMixin, UpdateView):
    """ View for updating a category """
    template_name = 'fyle/employee_form.html'
    model = Employee
    fields = ['code1', 'code2', 'code3']
    success_url = reverse_lazy('employee_list')
    success_message = 'Employee <strong>%(full_name)s</strong> has been ' \
                      'updated successfully'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            full_name=self.object.full_name,
        )


class ExpenseListView(ListView):
    """ View for listing of Expenses """
    template_name = 'fyle/expense_list.html'
    model = Expense
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        """ Show only current user data """
        queryset = super().get_queryset()
        queryset.filter(user=self.request.user).select_related('employee')
        return queryset


class ExpenseDetailView(DetailView):
    """ View for detail of Expenses """
    template_name = 'fyle/expense_detail.html'
    model = Expense

    def get_queryset(self):
        """ Show only current user data """
        queryset = super().get_queryset()
        queryset.filter(user=self.request.user).\
            select_related('employee').select_related('costcenter').\
            select_related('project')
        return queryset


class AdvanceListView(ListView):
    """ View for listing of advances """
    template_name = 'fyle/advance_list.html'
    model = Advance
    paginate_by = 10
    ordering = ['-issued_at']

    def get_queryset(self):
        """ Show only current user data """
        queryset = super().get_queryset()
        queryset.filter(user=self.request.user).\
            select_related('employee').select_related('project')
        return queryset


class AdvanceDetailView(DetailView):
    """ View for detail of Expenses """
    template_name = 'fyle/advance_detail.html'
    model = Advance

    def get_queryset(self):
        """ Show only current user data """
        queryset = super().get_queryset()
        queryset.filter(user=self.request.user).\
            select_related('employee').select_related('project')
        return queryset