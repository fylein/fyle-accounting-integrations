from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import JSONField
from django.db import models

from accounting_integrations.general.models import File
from accounting_integrations.fyle.models import ImportBatch


class ExportSetting(models.Model):
    """ Model for saving Export settings for a user """
    driver = models.CharField(max_length=100)
    driver_data = JSONField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class ExportBatch(models.Model):
    """ Model for recording the Export Batch Jobs """

    STATUS_CHOICES = (
        ('S', 'Started'),
        ('PR', 'Prepared'),
        ('PU', 'Pushed'),
        ('F', 'Failed'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default='S')
    detailed_status = models.TextField(null=True, blank=True)
    import_batch = models.OneToOneField(ImportBatch, on_delete=models.CASCADE)
    files = GenericRelation(File)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

