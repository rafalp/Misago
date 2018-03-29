"""
Create superuser for the devforum
"""

import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'devforum.settings'
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()


if User.objects.count() == 0:
    User.objects.create_superuser(
        os.environ['SUPERUSER_USERNAME'],
        os.environ['SUPERUSER_EMAIL'],
        password=os.environ['SUPERUSER_PASSWORD']
    )
