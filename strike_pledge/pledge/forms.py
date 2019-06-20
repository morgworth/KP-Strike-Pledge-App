# sendemail/forms.py
from django import forms

class PledgeForm(forms.Form):
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'firstname.(initial).lastname'}))

class ValidateForm(forms.Form):
    email_hash = forms.CharField(max_length=200, widget=forms.HiddenInput(), label='')
    work_email = forms.CharField(max_length=200, widget=forms.HiddenInput(), label='')
    region_list = (
        ('none', 'Kaiser Region'),
        ('norcal', 'California - Northern'),
        ('socal', 'California - Southern'),
        ('colorado', 'Colorado'),
        ('georgia', 'Georgia'),
        ('hawaii', 'Hawaii'),
        ('maryland', 'Maryland'),
        ('oregon', 'Oregon'),
        ('virginia', 'Virginia'),
        ('dc', 'Washington DC'),
        ('washington', 'Washington State')
    )
    kaiser_region = forms.ChoiceField(choices=region_list, required=True, label='')
    union_list = (
        ('none', 'Member of a Coalition union?'),
        ('yes', 'Yes'),
        ('no', 'No (sympathy striker)')
    )
    union_member = forms.ChoiceField(choices=union_list, required=True, label='')
    tweet = forms.CharField(max_length=245, required=False, initial='', label='', widget=forms.Textarea(attrs={'placeholder':'Why are you joining the strike? (optional)'}))
    personal_email=forms.EmailField(required=False, label='', initial='', widget=forms.TextInput(attrs={'placeholder':'Personal email (optional)'}))

class ReferralForm(forms.Form):
    email1 = forms.CharField(required=False)
    email2 = forms.CharField(required=False)
    email3 = forms.CharField(required=False)
