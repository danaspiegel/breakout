from django.conf.urls.defaults import *
from views import rules_list

urlpatterns = patterns('',
    url(r'^$', rules_list, name='robots_rule_list'),
)
