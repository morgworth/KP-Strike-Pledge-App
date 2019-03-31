from django.contrib import admin
from django.urls import path

from .views import emailView, successView, invalidEmailView, validateView

urlpatterns = [
    path('email/', emailView, name='email'),
    path('success/', successView, name='success'),
    path('invalid/', invalidEmailView, name='invalid'),
    path('validate/', validateView, name='validate'),
]
