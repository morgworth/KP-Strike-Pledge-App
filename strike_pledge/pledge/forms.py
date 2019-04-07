# sendemail/forms.py
from django import forms

class PledgeForm(forms.Form):
    email = forms.EmailField(required=True)
	
class ValidateForm(forms.Form):
    email_hash = forms.CharField(max_length=200, widget=forms.HiddenInput())
    SEIU_member = forms.BooleanField(required=False)
    personal_email=forms.EmailField(required=False, initial='')
    personal_phone = forms.CharField(max_length=20, required=False, initial='')
    region_list = (
        ('none', 'Not Specified'),
        ('norcal', 'Northern California'),
        ('socal', 'Southern California'),
        ('colorado', 'Colorado'),
        ('georgia', 'Georgia'),
        ('hawaii', 'Hawaii'),
        ('virginia', 'Virginia'),
        ('dc', 'Washington DC'),
        ('maryland', 'Maryland'),
        ('oregon', 'Oregon'),
        ('washington', 'Washington State')
    )
    Kaiser_region = forms.ChoiceField(choices=region_list, required=False)
