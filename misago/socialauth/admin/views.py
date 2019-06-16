from django.utils.translation import gettext_lazy as _

from ...admin.views import generic
from ..models import SocialAuthProvider
from ..providers import providers


class SocialAuthProviderAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:settings:socialauth:index"
    model = SocialAuthProvider
    form_class = None
    templates_dir = "misago/admin/socialauth"
    message_404 = _("Requested social login provider does not exist.")


class SocialAuthProvidersList(SocialAuthProviderAdmin, generic.ListView):
    def get_queryset(self):
        return list(super().get_queryset().filter(is_active=True))

    def process_context(self, request, context):
        context["inactive_providers"] = providers.list()
        return context


class EditSocialAuthProvider(SocialAuthProviderAdmin, generic.ModelFormView):
    message_submit = _("%(name)s social login has been updated.")

    def get_target(self, kwargs):
        try:
            return SocialAuthProvider.objects.get(provider=kwargs["pk"])
        except SocialAuthProvider.DoesNotExist:
            if not providers.is_registered(kwargs["pk"]):
                raise
            return SocialAuthProvider(provider=kwargs["pk"])

    def get_form_class(self, request, target):
        return providers.get_form_class(target.provider)

    def get_form(self, form_class, request, target):
        if request.method == "POST":
            return form_class(request.POST, request.FILES, instance=target)
        return form_class(instance=target, initial=target.settings)

    def get_template_name(self, request, target):
        return providers.get_template_name(target.provider)
