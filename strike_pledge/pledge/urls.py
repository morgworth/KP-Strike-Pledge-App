from django.contrib import admin
from django.urls import path

from .views import emailView, successView, validateView, aboutView, termsView, privacyView, faqView, homeView, confirmView, confirm2View, unionView, helpView, helpsuccessView, alreadySubmittedView


urlpatterns = [
    path('email/', emailView, name='email'),
    path('success/', successView, name='success'),
    path('success2/', success2View, name='success2'),
    path('validate/', validateView, name='validate'),
	path('about/', aboutView, name='about'),
    path('terms/', termsView, name='terms'),
	path('privacy/', privacyView, name='privacy'),
    path('faq/', faqView, name='faq'),
	path('', homeView, name='home'),
	path('confirm/', confirmView, name='confirm'),
    path('confirm2/', confirm2View, name='confirm2'),
	path('union/', unionView, name='union'),
    path('help/', helpView, name='help'),
    path('helpsuccess/', helpsuccessView, name='helpsuccess'),
	path('alreadysubmitted/', alreadySubmittedView, name='alreadysubmitted'),
]
