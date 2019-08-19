# sendemail/forms.py
from django import forms

class PledgeForm(forms.Form):
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'first.(m).last','size':10}))

class ValidateForm(forms.Form):
    email_hash = forms.CharField(max_length=200, widget=forms.HiddenInput(), label='')
    work_email = forms.CharField(max_length=200, widget=forms.HiddenInput(), label='')
    region_list = (
        ('none', '-----'),
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
        ('none', '-----'),
        ('yes', 'Yes'),
        ('no', 'No (sympathy striker)')
    )
    union_member = forms.ChoiceField(choices=union_list, required=True, label='')
    tweet = forms.CharField(max_length=237, required=False, initial='', label='', widget=forms.Textarea(attrs={'placeholder':'Your comment will be tweeted anonymously, along with "#kaiserstrike #wearekaiserworkers @aboutKP'}))
    personal_email = forms.EmailField(required=False, label='', initial='', widget=forms.TextInput(attrs={'placeholder':'janemdoe@email.com'}))

class ReferralForm(forms.Form):
    referrer = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Jane','size':22}))
    email1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'johndoe@email.com','size':22}))
    email2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'johndoe@email.com','size':22}))
    email3 = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'johndoe@email.com','size':22}))
    email4 = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'johndoe@email.com','size':22}))
    email5 = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'johndoe@email.com','size':22}))

class HelpForm(forms.Form):
    question = forms.CharField(max_length=300, required=True, initial='', label='', widget=forms.Textarea())
    home_email = forms.EmailField(required=True, label='', initial='', widget=forms.TextInput(attrs={'placeholder':'janemdoe@email.com','size':22}))
