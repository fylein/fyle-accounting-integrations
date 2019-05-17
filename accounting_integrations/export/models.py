from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import JSONField
from django.db import models

from accounting_integrations.general.models import File


class ExportSetting(models.Model):
    """ Model for saving Export settings for a user """
    driver = models.CharField(max_length=100)
    driver_data = JSONField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class ExportBatch(models.Model):
    """ Model for recording the Export Batch Jobs """
    created_at = models.DateTimeField(auto_now_add=True)
    files = GenericRelation(File)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

