"""
WSGI config for sitefordriver project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
#переключаем точки входа Джанго на новые настройки - local.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sitefordriver.settings.local')

application = get_wsgi_application()
