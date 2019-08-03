from django.contrib import admin
from django.urls import path

from .views import emailView, successView, validateView, aboutView, termsView, privacyView, faqView, homeView, confirmView, confirm2View, unionView, contactView, contactsuccessView, alreadySubmittedView, success2View, inviteView, invite2View


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
    path('contact/', contactView, name='contact'),
    path('contactsuccess/', contactsuccessView, name='contactsuccess'),
	path('alreadysubmitted/', alreadySubmittedView, name='alreadysubmitted'),
    path('invite/', inviteView, name='invite'),
    path('invite2/', invite2View, name='invite2'),
]
