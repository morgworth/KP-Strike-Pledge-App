from django.db import models

class Pledge(models.Model):
    email_hash = models.CharField(max_length=200, blank=False, unique=True)
    seiu_member = models.BooleanField(blank=True, null=True)
    region = models.CharField(max_length=100, blank=True)
    pers_email = models.CharField(max_length=200, blank=True)
    pers_phone = models.CharField(max_length=20, blank=True)
