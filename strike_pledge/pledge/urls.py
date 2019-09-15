from django.contrib import admin
from django.urls import path

from .views import successView, validateView, termsView, privacyView, homeView, confirmView, hiddenView

urlpatterns = [
    path('success/', successView, name='success'),
    path('validate/', validateView, name='validate'),
    path('terms/', termsView, name='terms'),
    path('privacy/', privacyView, name='privacy'),
    path('', homeView, name='home'),
    path('confirm/', confirmView, name='confirm'),
    path('hidden/', hiddenView, name='hidden')]
