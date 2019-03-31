from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pledge.models import Pledge
from pledge.serializers import PledgeSerializer
import hashlib

def emailView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = 'Please validate your email to count it with the pledges.'
            union = form.cleaned_data['union']
            email = form.cleaned_data['email']
			
            if 'kaiserpermanente.com' not in email:
                return redirect('invalid')
			
            
            hashed_email = hashlib.sha1(email.lower().encode()).hexdigest()
            validate_link = 'http://localhost:8000/validate/?u={u}&e={e}'.format(e=hashed_email, u=union)
            message = 'Please click the following link to validate your email: \n' + validate_link
            try:
                send_mail(subject, message, 'admin@example.com', [email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "email.html", {'form': form, 'count': Pledge.objects.all().count})

def successView(request):
    return HttpResponse('Please follow the link sent to your email to validate your pledge.')

def invalidEmailView(request):
    return HttpResponse('Invalid email. Email must be from Kaiser Permanente.')

@api_view(['GET'])
def validateView(request):
    email_hash = request.GET['e']
    union = request.GET['u']
    #pledge, created = Pledge.objects.update_or_create(email_hash=email_hash, union=union)
    try:
        pledge = Pledge.objects.get(email_hash=email_hash)
        pledge.union=union
        pledge.save()
    except Pledge.DoesNotExist:
        Pledge.objects.create(email_hash=email_hash, union=union)
    return HttpResponse('Your pledge has been counted! Solidarity!')