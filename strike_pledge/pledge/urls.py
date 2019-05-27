from django.contrib import admin
from django.urls import path

from .views import emailView, successView, validateView, aboutView, termsView, privacyView

urlpatterns = [
    path('', emailView, name='email'),
    path('success/', successView, name='success'),
    path('validate/', validateView, name='validate'),
	path('about/', aboutView, name='about'),
    path('terms/', termsView, name='terms'),
	path('privacy/', privacyView, name='privacy'),
]
