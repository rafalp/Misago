from django.conf import settings
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import pgettext
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from ..users.forms.auth import AuthenticationForm
from .nextpage import clean_next_page_url, get_next_page_url


class LoginView(View):
    template_name: str = "misago/auth/login_page.html"
    form_type = AuthenticationForm

    def dispatch(self, request: HttpRequest, **kwargs) -> HttpResponse:
        if request.settings.enable_oauth2_client:
            raise PermissionDenied(
                pgettext("login", "Please use %(provider)s to sign in.")
                % {"provider": request.settings.oauth2_provider}
            )

        return super().dispatch(request, **kwargs)

    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        form = self.form_type(request=request)
        return self.render(request, form, kwargs)

    def post(self, request: HttpRequest, **kwargs) -> HttpResponse:
        form = self.form_type(request.POST, request=request)
        if form.is_valid():
            return self.handle_valid_form(request, form, kwargs)

        if form.user_ban:
            pass

        return self.render(request, form, kwargs)

    def handle_valid_form(
        self, request: HttpRequest, form: AuthenticationForm, kwargs: dict
    ) -> HttpResponse:
        user = form.user_cache

        auth.login(request, user)

        if kwargs.get("next"):
            if next_page_url := clean_next_page_url(request, kwargs["next"]):
                return redirect(next_page_url)

        if next_page_url := get_next_page_url(request):
            return redirect(next_page_url)

        return redirect(settings.LOGIN_REDIRECT_URL)

    def render(
        self, request: HttpRequest, form: AuthenticationForm, kwargs: dict
    ) -> HttpResponse:
        context = {"form": form}

        if kwargs.get("message"):
            context["form_header"] = kwargs["message"]

        if kwargs.get("next"):
            context["next_page_url"] = clean_next_page_url(request, kwargs["next"])
        else:
            context["next_page_url"] = get_next_page_url(request)

        return render(request, self.template_name, context)


login_view = sensitive_post_parameters()(never_cache(LoginView.as_view()))
