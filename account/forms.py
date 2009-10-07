# This was taken from django-registration (mostly, anyway)

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import django.contrib.auth.forms
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.utils.http import int_to_base36
from django.utils.translation import ugettext_lazy as _

from django_mailer import send_email

from models import UserProfile

from lifestream.models import TwitterUser

# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = { 'class': 'required' }

class PasswordResetForm(django.contrib.auth.forms.PasswordResetForm):
    # Override the django.contrib.auth.forms.PasswordResetForm save function
    def save(self, domain_override=None, email_template_name=None, use_https=False, token_generator=default_token_generator):
        """
        Generates a one-use only link for resetting password and sends to the user
        """
        for user in self.users_cache:
            current_site = Site.objects.get_current()
            site_name = current_site.name
            domain = current_site.domain
            context = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
        send_email(user.email, context, 
                    subject_template_file='account/password_reset_email_subject.txt', 
                    text_template_file='account/password_reset_email_body.txt', 
                    html_template_file='account/password_reset_email_body.html')


class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    """
    first_name = forms.CharField(label=_(u'First Name'), max_length=30)
    last_name = forms.CharField(label=_(u'Last Name'), max_length=30)
    username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_(u'Choose a Username'))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_(u'Email address'))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'Password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'Password (again)'))
    age = forms.IntegerField(label=_(u'Age'), required=False, min_value=0, max_value=150)
    gender = forms.TypedChoiceField(label=_(u'Gender'), widget=forms.RadioSelect(), required=False, empty_value=None, choices=UserProfile.GENDER_CHOICES)
    occupation = forms.CharField(label=_(u'Occupation'), required=False, max_length=100)
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                             label=_(u'I have read and agree to the Terms of Service'),
                             error_messages={ 'required': u"You must agree to the terms to register." })

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_(u'This username is already taken. Please choose another.'))
    
    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password each time'))
        return self.cleaned_data
    
    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['username'], 
                                        password=self.cleaned_data['password1'], 
                                        email=self.cleaned_data['email'])
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password1'])
        return user

class ServicesForm(forms.Form):
    twitter_screen_name = forms.RegexField(regex=r'^\w*$', max_length=50, widget=forms.TextInput(attrs=attrs_dict), label=_(u'Enter Your Twitter Username'))
    
    def save(self):
        if self.cleaned_data['twitter_screen_name']:
            twitter_user, created = TwitterUser.objects.get_or_create(screen_name=self.cleaned_data['twitter_screen_name'])
            return twitter_user
        else:
            return None

