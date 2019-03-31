from django.db import models

class Pledge(models.Model):
    email_hash = models.CharField(max_length=200, blank=False, unique=True)
    union = models.CharField(max_length=100, blank=False)
