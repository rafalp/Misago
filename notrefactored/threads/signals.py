import django.dispatch

move_thread = django.dispatch.Signal(providing_args=["move_to"])
move_post = django.dispatch.Signal(providing_args=["move_to"])
merge_thread = django.dispatch.Signal(providing_args=["new_thread", "merge"])
merge_post = django.dispatch.Signal(providing_args=["new_post"])