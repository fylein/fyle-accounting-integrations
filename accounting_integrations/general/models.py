from django.conf import settings
from django.db import models


class GeneralSetting(models.Model):
    """ Model for saving General setting for a user """
    notification_emails = models.TextField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
