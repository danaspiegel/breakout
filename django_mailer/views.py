from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sites.models import Site, RequestSite
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext

from django_mailer.forms import PasswordResetForm

def password_reset(request, is_admin_site=False, template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        password_reset_form=PasswordResetForm, token_generator=default_token_generator,
        post_reset_redirect=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('django.contrib.auth.views.password_reset_done')
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {}
            opts['use_https'] = request.is_secure()
            opts['token_generator'] = token_generator
            if is_admin_site:
                opts['domain_override'] = request.META['HTTP_HOST']
            else:
                opts['email_template_name'] = email_template_name
                if not Site._meta.installed:
                    opts['domain_override'] = RequestSite(request).domain
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))

