"""
WSGI config for herri project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os

HERRI_PATH = '/opt/herri/server/herri/'

import sys
if not HERRI_PATH in sys.path:
    sys.path.append(HERRI_PATH)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "herri.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
