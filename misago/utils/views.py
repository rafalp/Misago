from django.core.urlresolvers import reverse
from django.shortcuts import redirect

def redirect_message(request, message, type='info', owner=None):
    """
    Set flash message and redirect to board index.
    """
    request.messages.set_flash(message, type, owner)
    return redirect(reverse('index'))