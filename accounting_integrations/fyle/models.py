from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import JSONField

from accounting_integrations.general.models import File


class Project(models.Model):
    """Model for saving project data from the Fyle API """
    id = models.CharField(primary_key=True, max_length=50)
    name = models.TextField(null=True)
    description = models.TextField(null=True)
    active = models.BooleanField()
    code1 = models.TextField(null=True, blank=True)
    code2 = models.TextField(null=True, blank=True)
    code3 = models.TextField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class CostCenter(models.Model):
    """Model for saving cost center data from the Fyle API """

    id = models.CharField(primary_key=True, max_length=50)
    name = models.TextField(null=True)
    description = models.TextField(null=True)
    code1 = models.TextField(null=True, blank=True)
    code2 = models.TextField(null=True, blank=True)
    code3 = models.TextField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Category(models.Model):
    """Model for saving category data from the Fyle API """

    id = models.IntegerField(primary_key=True)
    name = models.TextField(null=True)
    code = models.TextField(null=True)
    fyle_category = models.TextField(null=True)
    sub_category = models.TextField(null=True)
    enabled = models.BooleanField()
    code1 = models.TextField(null=True, blank=True)
    code2 = models.TextField(null=True, blank=True)
    code3 = models.TextField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Employee(models.Model):
    """Model for saving employee data from the Fyle API """

    id = models.CharField(primary_key=True, max_length=50)
    employee_email = models.EmailField(null=True)
    employee_code = models.TextField(null=True)
    full_name = models.TextField(null=True)
    location = models.TextField(null=True)
    level = models.TextField(null=True)
    business_unit = models.TextField(null=True)
    department = models.TextField(null=True)
    sub_department = models.TextField(null=True)
    title = models.TextField(null=True)
    default_cost_center = models.ForeignKey(
        CostCenter, on_delete=models.SET_NULL, null=True)
    disabled = models.BooleanField()
    org_id = models.TextField(null=True)
    org_name = models.TextField(null=True)
    code1 = models.TextField(null=True, blank=True)
    code2 = models.TextField(null=True, blank=True)
    code3 = models.TextField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Expense(models.Model):
    """Model for saving expense data from the Fyle API """

    id = models.CharField(primary_key=True, max_length=50)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    currency = models.TextField(null=True)
    amount = models.FloatField(null=True)
    foreign_currency = models.TextField(null=True)
    foreign_amount = models.FloatField(null=True)
    purpose = models.TextField(null=True)
    custom_properties = JSONField(null=True)
    reimbursable = models.BooleanField()
    state = models.TextField(null=True)
    spent_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(null=True)
    approved_at = models.DateTimeField(null=True)
    verified = models.BooleanField()
    verified_at = models.DateTimeField(null=True)
    reimbursed_at = models.DateTimeField(null=True)
    vendor = models.TextField(null=True)
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True)
    cost_center = models.ForeignKey(
        CostCenter, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Advance(models.Model):
    """Model for saving advance data from the Fyle API """

    id = models.CharField(primary_key=True, max_length=50)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True)
    currency = models.TextField(null=True)
    amount = models.FloatField(null=True)
    purpose = models.TextField(null=True)
    issued_at = models.DateTimeField(null=True)
    payment_mode = models.TextField(null=True)
    original_currency = models.TextField(null=True)
    original_amount = models.FloatField(null=True)
    reference = models.TextField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class ImportBatch(models.Model):
    """ Model for recording the Import Batch Jobs """
    created_at = models.DateTimeField(auto_now_add=True)
    min_updated_at = models.DateTimeField(null=True, blank=True)
    max_updated_at = models.DateTimeField(null=True, blank=True)
    expenses = models.ManyToManyField(Expense)
    advances = models.ManyToManyField(Advance)
    files = GenericRelation(File)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class FyleSetting(models.Model):
    """Model for saving the Fyle Import Settings"""
    sync_frequency = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
