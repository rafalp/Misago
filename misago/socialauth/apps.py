from django.apps import AppConfig

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
            settings={"scope": ["email"]},
            admin_form=FacebookForm,
            admin_template="misago/admin/socialauth/facebook_form.html",
        )
        providers.add(
            provider="github",
            name="GitHub",
            settings={"scope": ["read:user", "user:email"]},
            admin_form=GitHubForm,
            admin_template="misago/admin/socialauth/github_form.html",
        )
        providers.add(
            provider="google",
            name="Google",
            admin_form=GoogleForm,
            admin_template="misago/admin/socialauth/google_form.html",
        )
        providers.add(
            provider="twitter",
            name="Twitter",
            admin_form=TwitterForm,
            admin_template="misago/admin/socialauth/twitter_form.html",
        )
