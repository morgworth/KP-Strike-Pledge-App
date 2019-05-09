from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import PledgeForm, ValidateForm
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pledge.models import Pledge
from pledge.serializers import PledgeSerializer
import hashlib
import twitter

def emailView(request):
    if request.method == 'GET':
        form = PledgeForm()
    else:
        form = PledgeForm(request.POST)
        if form.is_valid():
            subject = 'Please validate your email to count it with the pledges.'
            email = form.cleaned_data['email'] + '@kp.org'
            hashed_email = hashlib.sha1(email.lower().encode()).hexdigest()
            validate_link = 'http://localhost:8000/validate/?&e={e}'.format(e=hashed_email)
            message = 'Please click the following link to validate your email: \n' + validate_link
            try:
                send_mail(subject, message, 'admin@example.com', [email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "email.html", {'form': form, 'count': Pledge.objects.all().count})

def successView(request):
    
	return render(request,"success.html",{'count': Pledge.objects.all().count})

def validateView(request):
    if request.method == 'GET':
        email_hash = request.GET['e']
        form = ValidateForm(initial={'email_hash': email_hash})
    else:
        form = ValidateForm(request.POST)
        if form.is_valid():
            email_hash = form.cleaned_data['email_hash']
            seiu_member = form.cleaned_data['SEIU_member']
            region = form.cleaned_data['Kaiser_region']
            pers_email = form.cleaned_data['personal_email']
            pers_phone = form.cleaned_data['personal_phone']
            tweet = form.cleaned_data['tweet']
            if tweet != '':
                api = twitter.Api(consumer_key='8nzLUS0rK3WKxe3lKaWkO6SXS',
								  consumer_secret='UxrSothiwP1jWibu4ElXHAXtzhBlSWRCJuPbTrxrfu9h0JBYYZ',
								  access_token_key='1117328256473026561-PjDxLe616snf93kFbjCAdDkHM8aHNQ',
								  access_token_secret='j2Cw2DZ4LFBsEnYDMXHrTsgeFys3fPupZcdOUpSJzVQzK')
                api.PostUpdate(tweet[0:280])
            try:
                pledge = Pledge.objects.get(email_hash=email_hash)
                pledge.seiu_member = seiu_member
                pledge.region = region
                pledge.pers_email = pers_email
                pledge.pers_phone = pers_phone
                pledge.message = tweet
                pledge.save()
            except Pledge.DoesNotExist:
                Pledge.objects.create(email_hash = email_hash,
                                      seiu_member = seiu_member, 
									  region = region, 
									  pers_email = pers_email, 
									  pers_phone = pers_phone,
                                      message = tweet)
            return redirect('email')				
    return render(request, "contact.html", {'form': form})

def aboutView(request):
    return render(request, "about.html")

def faqView(request):
    return render(request, "faq.html")
