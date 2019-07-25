from django.apps import AppConfig
from social_core.backends.facebook import FacebookOAuth2
from social_core.backends.github import GithubOAuth2
from social_core.backends.google import GoogleOAuth2
from social_core.backends.twitter import TwitterOAuth

from .providers import providers


class MisagoSocialAuthConfig(AppConfig):
    name = "misago.socialauth"
    label = "misago_socialauth"
    verbose_name = "Misago Social Auth"

    def ready(self):
        # Register default providers
        from .admin.forms import FacebookForm, GitHubForm, GoogleForm, TwitterForm

        providers.add(
            provider="facebook",
            name="Facebook",
            auth_backend=FacebookOAuth2,
            settings={"scope": ["email"]},
            admin_form=FacebookForm,
            admin_template="misago/admin/socialauth/form.html",
        )
        providers.add(
            provider="github",
            name="GitHub",
            auth_backend=GithubOAuth2,
            settings={"scope": ["read:user", "user:email"]},
            admin_form=GitHubForm,
            admin_template="misago/admin/socialauth/form.html",
        )
        providers.add(
            provider="google",
            name="Google",
            auth_backend=GoogleOAuth2,
            admin_form=GoogleForm,
            admin_template="misago/admin/socialauth/form.html",
        )
        providers.add(
            provider="twitter",
            name="Twitter",
            auth_backend=TwitterOAuth,
            admin_form=TwitterForm,
            admin_template="misago/admin/socialauth/form.html",
        )
