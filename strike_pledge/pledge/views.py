from django.core.mail import send_mail, BadHeaderError
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import PledgeForm, ValidateForm, ReferralForm, HelpForm
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pledge.models import Pledge
from pledge.serializers import PledgeSerializer
import hashlib
import twitter
import urllib
import os
import requests

def homeView(request):
    count = Pledge.objects.all().count()
    #if count < 1000:
    #    count = '< 1,000'

    if request.method == 'GET':
        form = PledgeForm()
    else:
        form = PledgeForm(request.POST)
        if form.is_valid():
            #subject = 'Confirm your strike pledge'
            subject = 'signup'
            proto_username = form.cleaned_data['email']
            pre_username = proto_username.lower()
            sep1 = '@'
            username = pre_username.split(sep1, 1)[0]
            sep2 = '.'
            #first_name = username.split(sep2, 1)[0].title()
            email = username + '@kp.org'
            hashed_email = hashlib.sha1(email.encode()).hexdigest()
            validate_link = 'kaiserstrike(dot)org/validate/?u={u}&e={e}'.format(u=username,e=hashed_email)
            message = pre_username
            #message = 'Hi ' + first_name
            #message += '\n\nYou or your co-worker indicated you want to make a strike pledge.\n\n'
            #message += 'Open this webpage to complete your pledge and post a tweet. If you can\'t open the page, or if you have privacy concerns, forward this email to a personal account and open the link on a personal phone or computer.\n\n'
            #message += validate_link
            #message += '\n\n\n\n\nFrom,\n\n'
            #message += 'Your co-workers and friends at kaiserstrike(dot)org'
            #message += '\n\nP.S.: Feel free to reply to this email with any questions.'
            try:
                Pledge.objects.get(email_hash=hashed_email)
            except Pledge.DoesNotExist:
                try:
                    send_mail(subject, message, 'pledge <pledge@mail.kaiserstrike.org>', ['signups@kaiserstrike.org'], fail_silently=True)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                except Exception:
                    print('')
                return redirect('success')
    return render(request, "home.html", {'form': form, 'count': count})

def successView(request):
    return render(request, "success.html")

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
                        api.PostUpdate(tweet[0:246] + ' #wearekaiserworkers #kaiserstrike')
                    except:
                        print('')
                try:
                    pledge = Pledge.objects.get(email_hash=email_hash)
                    #pledge.union_member = union_member
                    #pledge.region = region
                    #pledge.pers_email = pers_email
                    #pledge.message = tweet
                    #pledge.save()
                    return redirect('home')
                except Pledge.DoesNotExist:
                    Pledge.objects.create(email_hash = email_hash,
                                      work_email = work_email,
                                      union_member = union_member,
									  region = region,
									  pers_email = pers_email,
                                      message = tweet)
                return redirect('confirm')
    return render(request, "contact.html", {'form': form, 'email_hash':email_hash, 'work_email':work_email })

def termsView(request):
    return render(request, "terms.html")

def privacyView(request):
    return render(request, "privacy.html")

def confirmView(request):
    return render(request, "confirmation.html")

def unionView(request):
    return render(request, "unions.html")

def hiddenView(request):
    if request.method == 'GET':
        form = PledgeForm()
    else:
        form = PledgeForm(request.POST)
        if form.is_valid():
            #subject = 'Complete your strike pledge'
            proto_username = form.cleaned_data['email']
            pre_username = proto_username.lower()
            sep1 = '@'
            username = pre_username.split(sep1, 1)[0]
            sep2 = '.'
            first_name = username.split(sep2, 1)[0].title()
            email = username + '@kaiserstrike.org' # restore - email = username + '@kp.org'
            to = first_name + ' <' + email + '>'
            hashed_email = hashlib.sha1(email.encode()).hexdigest()
            validate_link = 'kaiserstrike.org/validate/?u={u}&e={e}'.format(u=username,e=hashed_email)
            #message = 'Hi ' + first_name
            #message += '\n\nYou or your co-worker indicated you want to make a strike pledge and/or post to twitter, anonymously.\n\n'
            #message += 'To do so, click the link below. If you can\'t open the link, or if you have privacy concerns, forward this email to a personal account and open the link on a personal phone or computer.\n\n'
            #message += validate_link
            #message += '\n\n\n\n\nFrom,\n\n'
            #message += 'Your co-workers and friends at kaiserstrike(dot)org'
            #message += '\n\nP.S.: Feel free to reply to this email with any questions.'
            def send_simple_message():
            	return requests.post(
            		"https://api.mailgun.net/v3/mail.kaiserstrike.org/messages",
            		auth=("api", "key-07f2b930ea5cedd16324499e964f8742"),
            		data={"from": "pledge <pledge@mail.kaiserstrike.org>",
                        "to": to,
                        "subject": "Complete your strike pledge and/or post to twitter",
                        "template": "complete_pledge",
                        "v:first_name": first_name,
                        "v:link": validate_link})
            try:
                Pledge.objects.get(email_hash=hashed_email)
            except Pledge.DoesNotExist:
                try:
                    send_simple_message()
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                except Exception:
                    print('')
                return redirect('success')
    return render(request, "hidden.html", {'form': form})
