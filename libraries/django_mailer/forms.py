# Override the django.contrib.auth.forms.PasswordResetForm save function

import django.contrib.auth.forms
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36
from django.conf import settings
from django import forms

from profiles.models import BPUser

class PasswordResetForm(forms.Form):
    username = forms.CharField(label=_("Username"), max_length=30)

    def clean_username(self):
        """
        Validates that a user exists with the given e-mail address.
        """
        username = self.cleaned_data["username"]
        self.user_cache = BPUser.objects.get(username__iexact=username)
        if not self.user_cache:
            raise forms.ValidationError(_("That user doesn't exist. Are you sure you've registered?"))

    def save(self, domain_override=None, email_template_name=None, use_https=False, token_generator=default_token_generator):
        """
        Generates a one-use only link for resetting password and sends to the user
        """
        from notification import send_email
        from django.utils.http import int_to_base36
        from django.contrib.auth.tokens import default_token_generator
        
        site = Site.objects.get_current()
        context = {
            'email': self.user_cache.email,
            'site': site,
            'uid': int_to_base36(self.user_cache.id),
            'user': self.user_cache,
            'token': token_generator.make_token(self.user_cache),
            'protocol': use_https and 'https' or 'http',
        }
        send_email(self.user_cache.email, 
                    context, 
                    subject_template_file='registration/password_reset_email_subject.txt', 
                    text_template_file='registration/password_reset_email_body.txt', 
                    html_template_file='registration/password_reset_email_body.html')
