# sendemail/forms.py
from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    union = forms.ChoiceField(choices=[('seiu','SEIU'),('nurses', 'Nurse\'s Union'),('unaffiliated', 'No Union')], )