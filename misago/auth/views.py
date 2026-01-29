from django.conf import settings
from django.contrib import auth
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from ..core.exceptions import Banned
from ..users.forms.auth import AuthenticationForm
from .nextpage import clean_next_page_url, get_next_page_url
from .loginurl import get_login_url


class LoginView(View):
    template_name: str = "misago/auth/login_page.html"
    form_type = AuthenticationForm

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, request: HttpRequest, **kwargs) -> HttpResponse:
        if self.is_view_disabled():
            raise Http404()

        if request.user.is_authenticated:
            return self.get_next_page_redirect(request, kwargs)

        if request.settings.enable_oauth2_client:
            return delegated_login(
                request,
                message=kwargs.get("message"),
                status=kwargs.get("status", 200),
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
            raise Banned(form.user_ban)

        return self.render(request, form, kwargs)

    def handle_valid_form(
        self, request: HttpRequest, form: AuthenticationForm, kwargs: dict
    ) -> HttpResponse:
        user = form.user_cache
        auth.login(request, user)
        return self.get_next_page_redirect(request, kwargs)

    def get_next_page_redirect(
        self, request: HttpRequest, kwargs: dict
    ) -> HttpResponse:
        if kwargs.get("next"):
            if next_page_url := clean_next_page_url(request, kwargs["next"]):
                return redirect(next_page_url)

        elif next_page_url := get_next_page_url(request):
            return redirect(next_page_url)

        return redirect(settings.LOGIN_REDIRECT_URL)

    def render(
        self, request: HttpRequest, form: AuthenticationForm, kwargs: dict
    ) -> HttpResponse:
        context = {
            "form": form,
            "social_login": list(request.socialauth.values()),
        }

        if kwargs.get("message"):
            context["form_header"] = kwargs["message"]

        if "next" not in kwargs:
            context["next_page_url"] = get_next_page_url(request)

        return render(
            request,
            self.template_name,
            context,
            status=kwargs.get("status", 200),
        )

    def is_view_disabled(self) -> bool:
        return is_misago_login_page_disabled()


login = LoginView.as_view()


def delegated_login(
    request: HttpRequest, *, message: str | None = None, status: int = 200
):
    return render(
        request,
        "misago/auth/delegated_page.html",
        {"form_header": message},
        status=status,
    )


def is_misago_login_page_disabled() -> bool:
    return get_login_url() != reverse("misago:login")
