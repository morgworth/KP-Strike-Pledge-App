from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import PledgeForm, ValidateForm, ReferralForm
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pledge.models import Pledge
from pledge.serializers import PledgeSerializer
import hashlib
import twitter
import urllib
import os

def emailView(request):
    if request.method == 'GET':
        form = PledgeForm()
    else:
        form = PledgeForm(request.POST)
        if form.is_valid():
            subject = 'Confirm your strike pledge'
            username = form.cleaned_data['email']
            email = username + '@kp.org'
            hashed_email = hashlib.sha1(email.lower().encode()).hexdigest()
            validate_link = 'kaiserstrike.org/validate/?u={u}&e={e}'.format(u=username,e=hashed_email)
            message = 'Hello!\n\nYou or your co-worker indicated you want to join the Oct/Nov 2019 Kaiser strike.\n\n'
            message += 'Click on this link to make a digital strike pledge and to tweet using our handle (@kaiserstrike19):\n\n'
            message += validate_link
            message += '\n\n\n\n\nFrom,\n\n'
            message += 'Your co-workers and friends at kaiserstrike(dot)org'
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
    return render(request, "email.html", {'form': form})

def successView(request):
	return render(request,"success.html")

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
            if email_hash == hashlib.sha1(work_email.lower().encode()).hexdigest():
                union_member = form.cleaned_data['union_member']
                region = form.cleaned_data['kaiser_region']
                pers_email = form.cleaned_data['personal_email']
                tweet = form.cleaned_data['tweet']
                if tweet != '':
                    api = twitter.Api(consumer_key=os.environ['consumer_key'],
								  consumer_secret=os.environ['consumer_secret'],
								  access_token_key=os.environ['access_token_key'],
								  access_token_secret=os.environ['access_token_secret'])
                    try:
                        api.PostUpdate(tweet[0:235] + '...#kaiserstrike #wearekaiserworkers @aboutKP')
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
                return redirect('confirm')
    return render(request, "contact.html", {'form': form, 'email_hash':email_hash, 'work_email':work_email })

def aboutView(request):
    return render(request, "about.html")

def faqView(request):
    return render(request, "faq.html")

def termsView(request):
    return render(request, "terms.html")

def privacyView(request):
    return render(request, "privacy.html")

def homeView(request):
    count = Pledge.objects.all().count()
    #if count < 1000:
    #    count = '< 1,000'
    return render(request, "home.html", {'count': count})

def confirmView(request):
    if request.method == 'GET':
        form = ReferralForm
    else:
        form = ReferralForm(request.POST)
        if form.is_valid():
            email1 = form.cleaned_data['email1']
            email2 = form.cleaned_data['email2']
            email3 = form.cleaned_data['email3']
            email4 = form.cleaned_data['email4']
            email5 = form.cleaned_data['email5']
            subject = 'Make a digital strike pledge'
            message = 'Hello!\n\nYour co-worker indicated you want to join the Oct/Nov 2019 Kaiser strike.\n\n'
            message += 'Click on this link to make a digital strike pledge and to tweet using our handle (@kaiserstrike19):\n\n'
            message += 'https://kaiserstrike.org'
            message += '\n\n\n\n\nFrom,\n\n'
            message += 'Your co-workers and friends at kaiserstrike(dot)org'
            if email1 != '':
                try:
                    send_mail(subject, message, 'noreply <noreply@kaiserstrike.org>', [email1], fail_silently=True)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                except Exception:
                    print('')
            if email2 != '':
                try:
                    send_mail(subject, message, 'noreply <noreply@kaiserstrike.org>', [email2], fail_silently=True)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                except Exception:
                    print('')
            if email3 != '':
                try:
                    send_mail(subject, message, 'noreply <noreply@kaiserstrike.org>', [email3], fail_silently=True)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                except Exception:
                    print('')
            if email4 != '':
                try:
                    send_mail(subject, message, 'noreply <noreply@kaiserstrike.org>', [email2], fail_silently=True)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                except Exception:
                    print('')
            if email5 != '':
                try:
                    send_mail(subject, message, 'noreply <noreply@kaiserstrike.org>', [email2], fail_silently=True)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                except Exception:
                    print('')
                return redirect('home')
    return render(request, "confirmation.html", {'form':form})

def unionView(request):
    return render(request, "unions.html")
