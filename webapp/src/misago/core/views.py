from django.shortcuts import redirect


def forum_index(request):
    return  # blow up as this view is normally non-reachable!


def home_redirect(*args, **kwargs):
    return redirect("misago:index")
