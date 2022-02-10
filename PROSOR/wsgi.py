"""
WSGI config for PROSOR project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from configparser import RawConfigParser
config = RawConfigParser()
initfile = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'settings.ini')
config.read(initfile)

os.environ.setdefault('DJANGO_SETTINGS_MODULE',  config.get('ENV', 'SETTING_FILE'))
print(config.get('ENV', 'SETTING_FILE'))

application = get_wsgi_application()
