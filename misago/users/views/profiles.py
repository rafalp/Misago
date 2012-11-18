from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from misago.users.models import User, Group
from misago.views import error404


def list(request):
    pass


def show(request, user, username):
    user = int(user)
    try:
        user = User.objects.get(pk=user)
        if user.username_slug != username:
            # Force crawlers to take notice of updated username
            return redirect(reverse('user', args=(user.username_slug, user.pk)), permanent=True)
        return request.theme.render_to_response('users/profile.html',
                                            {
                                             'profile': user,
                                            },
                                            context_instance=RequestContext(request));
    except User.DoesNotExist:
        return error404(request)