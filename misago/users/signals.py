import django.dispatch


delete_user_content = django.dispatch.Signal()
username_changed = django.dispatch.Signal()
