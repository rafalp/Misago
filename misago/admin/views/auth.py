from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from misago.admin import auth
from misago.users.forms.auth import AdminAuthenticationForm


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request):
    url_namespace = request.resolver_match.namespace
    form = AdminAuthenticationForm(request)

    if request.method == 'POST':
        form = AdminAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.user_cache)
            return redirect('%s:index' % url_namespace)

    return render(request, 'misago/admin/login.html',
                  {'form': form, 'namespace': url_namespace})
