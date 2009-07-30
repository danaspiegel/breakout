# Local development settings

# In order to make different settings work under django-admin.py or wsgi, you must set:
# export PYTHONPATH='.'
# export DJANGO_SETTINGS_MODULE='settings.local'

from settings.common import *

DEBUG = True
DEBUG_SQL = True
TEMPLATE_DEBUG = DEBUG
SEND_BROKEN_LINK_EMAILS = False

SECRET_KEY = 'p9*tezdjb6z02_sh_vx@+0va09=j4i3pi6!7tq*mxarzhwgd__'

DATABASE_NAME = 'breakout'
DATABASE_USER = 'breakout'
DATABASE_PASSWORD = 'breakout'
DATABASE_HOST = ''
DATABASE_PORT = ''

GOOGLE_MAPS_API_KEY = 'ABQIAAAAZ2jpq9DecEp8EYUNWHTHVxT2yXp_ZAY8_ufC3CFXhHIE1NvwkxRcoqYv4xXq3a1_eOXomt5P7tIRmQ'