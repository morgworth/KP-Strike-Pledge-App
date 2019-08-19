from django.contrib import admin
from django.urls import path

from .views import successView, validateView, termsView, privacyView, homeView, confirmView, unionView, success2View


urlpatterns = [
    path('success/', successView, name='success'),
    path('success2/', success2View, name='success2'),
    path('validate/', validateView, name='validate'),
    path('terms/', termsView, name='terms'),
	path('privacy/', privacyView, name='privacy'),
	path('', homeView, name='home'),
	path('confirm/', confirmView, name='confirm'),
	path('union/', unionView, name='union'),
]
