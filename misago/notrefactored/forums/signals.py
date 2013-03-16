import django.dispatch

move_forum_content = django.dispatch.Signal(providing_args=["move_to"])
delete_forum_content = django.dispatch.Signal()