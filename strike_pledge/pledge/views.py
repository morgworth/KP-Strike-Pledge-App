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
            validate_link = 'http://localhost:8000/validate/?u={u}&e={e}'.format(u=form.cleaned_data['email'],e=hashed_email)
            message = 'You or your co-worker indicated you\'d like to join the 2019 Kaiser strike in Oct/Nov. Please click the following link to finalize your strike pledge: \n' + validate_link
            message += '\n\n Tech Workers Coalition \n'
            message += 'A coalition of tech workers, labor organizers, community organizers, and friends working in solidarity with existing movements towards social justice, workers\' rights, and economic inclusion.'
            try:
                Pledge.objects.get(email_hash=hashed_email)
            except Pledge.DoesNotExist:
                try:
                    send_mail(subject, message, 'noreply <noreply@kaiserstrike.org>', [email], fail_silently=True)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                except Exception:
                    print('')
                return redirect('success')
    return render(request, "email.html", {'form': form, 'count': Pledge.objects.all().count})

def successView(request):
	return render(request,"success.html",{'count': Pledge.objects.all().count})

def validateView(request):
    if request.method == 'GET':
        email_hash = request.GET['e']
        work_email = request.GET['u']+'@kp.org'
        form = ValidateForm(initial={'email_hash': email_hash, 'work_email': work_email})
    elif request.method == 'POST':
        form = ValidateForm(request.POST)
        if form.is_valid():
            email_hash = form.cleaned_data['email_hash']
            work_email = form.cleaned_data['work_email']
            union_member = form.cleaned_data['union_member']
            region = form.cleaned_data['kaiser_region']
            pers_email = form.cleaned_data['personal_email']
            tweet = form.cleaned_data['tweet']
            if tweet != '' and Pledge.objects.all().count > 1000:
                api = twitter.Api(consumer_key=os.environ['consumer_key'],
								  consumer_secret=os.environ['consumer_secret'],
								  access_token_key=os.environ['access_token_key'],
								  access_token_secret=os.environ['access_token_secret'])
                try:
                    api.PostUpdate(tweet[0:245] + '... #kaiserstrike @aboutKP @KPShare')
                except:
                    print('')
            try:
                pledge = Pledge.objects.get(email_hash=email_hash)
                pledge.union_member = union_member
                pledge.region = region
                pledge.pers_email = pers_email
                pledge.message = tweet
                pledge.save()
            except Pledge.DoesNotExist:
                Pledge.objects.create(email_hash = email_hash,
                                      work_email = work_email,
                                      union_member = union_member, 
									  region = region, 
									  pers_email = pers_email, 
                                      message = tweet)
            return redirect('email')				
    return render(request, "contact.html", {'form': form})

def aboutView(request):
    return render(request, "about.html")

def faqView(request):
    return render(request, "faq.html")

def termsView(request):
    return render(request, "terms.html")

def privacyView(request):
    return render(request, "privacy.html")
