from django.apps import AppConfig

from .providers import providers


class MisagoSocialAuthConfig(AppConfig):
    name = "misago.socialauth"
    label = "misago_socialauth"
    verbose_name = "Misago Social Auth"

    def ready(self):
        # Register default providers
        from .admin.forms import FacebookForm

        providers.add(
            provider="facebook",
            name="Facebook",
            admin_form=FacebookForm,
            admin_template="misago/admin/socialauth/facebook_form.html",
        )
        providers.add(
            provider="twitter", name="Twitter", admin_form=None, admin_template=""
        )
        providers.add(
            provider="github", name="GitHub", admin_form=None, admin_template=""
        )
        providers.add(
            provider="google", name="Google", admin_form=None, admin_template=""
        )
