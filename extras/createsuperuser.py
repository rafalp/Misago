"""
Create superuser for the devproject
"""

import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'devproject.settings'
django.setup()

from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

User = get_user_model()


if User.objects.count() == 0:
    superuser = User.objects.create_superuser(
        os.environ['SUPERUSER_USERNAME'],
        os.environ['SUPERUSER_EMAIL'],
        get_random_string(10), # set throwaway password
        set_default_avatar=True,
    )

    # Override user's throwaway password with configured one
    superuser.set_password(os.environ['SUPERUSER_PASSWORD'])
    superuser.save()
