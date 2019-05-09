# sendemail/forms.py
from django import forms

class PledgeForm(forms.Form):
    email = forms.CharField(required=True)
	
class ValidateForm(forms.Form):
    email_hash = forms.CharField(max_length=200, widget=forms.HiddenInput())
    union_list = (
        ('none', 'Union / Non-union'),
        ('yes', 'Union'),
        ('no', 'Non-union')
    )
    union_member = forms.ChoiceField(choices=union_list, required=False)
    personal_email=forms.EmailField(required=False, initial='', widget=forms.TextInput(attrs={'placeholder':'Personal email address'}))
    region_list = (
        ('none', 'KP Region'),
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
    kaiser_region = forms.ChoiceField(choices=region_list, required=False)
    tweet = forms.CharField(max_length=280, required=False, initial='', widget=forms.Textarea(attrs={'placeholder':'Why are you going on strike? (optional)'}))
