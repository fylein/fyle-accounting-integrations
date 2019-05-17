from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class GeneralSetting(models.Model):
    """ Model for saving General setting for a user """
    notification_emails = models.TextField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class File(models.Model):
    """ Model for storing files of import and export batches"""
    type = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    contents = models.FileField(upload_to='files/%Y/%m/%d/')

    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    related_object = GenericForeignKey('content_type', 'object_id')
