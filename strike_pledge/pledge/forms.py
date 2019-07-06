# sendemail/forms.py
from django import forms

class PledgeForm(forms.Form):
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'first.(initial).last','size':22}))

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
    tweet = forms.CharField(max_length=235, required=False, initial='', label='', widget=forms.Textarea(attrs={'placeholder':'Why are you making a strike pledge? (optional)'}))
    personal_email=forms.EmailField(required=False, label='', initial='', widget=forms.TextInput(attrs={'placeholder':'Personal email (optional)'}))

class ReferralForm(forms.Form):
    email1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'janedoe@email.com','size':22}))
    email2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'johndoe@email.com','size':22}))
    email3 = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'janedoe@email.com','size':22}))
    email4 = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'johndoe@email.com','size':22}))
    email5 = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'janedoe@email.com','size':22}))

class HelpForm(forms.Form):
    question = forms.CharField(max_length=300, required=True, initial='', label='', widget=forms.Textarea())
    home_email = forms.EmailField(required=True, label='', initial='', widget=forms.TextInput(attrs={'size':22}))
