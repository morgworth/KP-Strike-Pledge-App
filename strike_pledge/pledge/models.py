from django.db import models

class Pledge(models.Model):
    email_hash = models.CharField(max_length=200, blank=False, unique=True)
    union_member = models.CharField(max_length=100, blank=True, default='none')
    region = models.CharField(max_length=100, blank=True)
    pers_email = models.CharField(max_length=200, blank=True)
    message = models.CharField(max_length=280, blank=True)
