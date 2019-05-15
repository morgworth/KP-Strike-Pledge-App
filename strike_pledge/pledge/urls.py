from django.contrib import admin
from django.urls import path

from .views import emailView, successView, validateView, aboutView, faqView, termsView, privacyView

urlpatterns = [
    path('email/', emailView, name='email'),
    path('success/', successView, name='success'),
    path('validate/', validateView, name='validate'),
	path('about/', aboutView, name='about'),
    path('faq/', faqView, name='faq'),
    path('terms/', termsView, name='terms'),
	path('privacy/', privacyView, name='privacy'),
]
