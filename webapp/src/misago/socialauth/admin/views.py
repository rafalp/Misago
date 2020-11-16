from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from ...admin.views import generic
from ..cache import clear_socialauth_cache
from ..models import SocialAuthProvider
from ..providers import providers


class SocialAuthProviderAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:settings:socialauth:index"
    model = SocialAuthProvider
    form_class = None
    templates_dir = "misago/admin/socialauth"
    message_404 = _("Requested social login provider does not exist.")

    def get_target(self, kwargs):
        queryset = SocialAuthProvider.objects.filter(is_active=True)
        if self.is_atomic:
            queryset = queryset.select_for_update()
        return queryset.get(pk=kwargs["pk"])

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class SocialAuthProvidersList(SocialAuthProviderAdmin, generic.ListView):
    def process_context(self, request, context):
        active_providers = [i.pk for i in context["items"]]
        context["inactive_providers"] = []
        for provider in providers.list():
            if provider["provider"] not in active_providers:
                context["inactive_providers"].append(provider)
        return context


class EditSocialAuthProvider(SocialAuthProviderAdmin, generic.ModelFormView):
    def get_target(self, kwargs):
        try:
            return SocialAuthProvider.objects.get(provider=kwargs["pk"])
        except SocialAuthProvider.DoesNotExist:
            if not providers.is_registered(kwargs["pk"]):
                raise
            return SocialAuthProvider(provider=kwargs["pk"])

    def get_form_class(self, request, target):
        return providers.get_admin_form_class(target.provider)

    def get_form(self, form_class, request, target):
        if request.method == "POST":
            return form_class(request.POST, instance=target, request=request)
        return form_class(instance=target, initial=target.settings, request=request)

    def get_template_name(self, request, target):
        return providers.get_admin_template_name(target.provider)

    def handle_form(self, form, request, target):
        form.save()
        clear_socialauth_cache()

        message = _("Login with %(provider)s has been updated.")
        messages.success(request, message % {"provider": target})


class DisableSocialAuthProvider(SocialAuthProviderAdmin, generic.ButtonView):
    def button_action(self, request, target):
        target.is_active = False
        target.save(update_fields=["is_active"])
        clear_socialauth_cache()

        message = _("Login with %(provider)s has been disabled.")
        messages.success(request, message % {"provider": target})


class MoveDownSocialAuthProvider(SocialAuthProviderAdmin, generic.ButtonView):
    def button_action(self, request, target):
        try:
            other_target = SocialAuthProvider.objects.filter(
                is_active=True, order__gt=target.order
            )
            other_target = other_target.earliest("order")
        except SocialAuthProvider.DoesNotExist:
            other_target = None

        if other_target:
            other_target.order, target.order = target.order, other_target.order
            other_target.save(update_fields=["order"])
            target.save(update_fields=["order"])
            clear_socialauth_cache()

            message = _("Login with %(provider)s has been moved after %(other)s.")
            targets_names = {"provider": target, "other": other_target}
            messages.success(request, message % targets_names)


class MoveUpSocialAuthProvider(SocialAuthProviderAdmin, generic.ButtonView):
    def button_action(self, request, target):
        try:
            other_target = SocialAuthProvider.objects.filter(
                is_active=True, order__lt=target.order
            )
            other_target = other_target.latest("order")
        except SocialAuthProvider.DoesNotExist:
            other_target = None

        if other_target:
            other_target.order, target.order = target.order, other_target.order
            other_target.save(update_fields=["order"])
            target.save(update_fields=["order"])
            clear_socialauth_cache()

            message = _("Login with %(provider)s has been moved before %(other)s.")
            targets_names = {"provider": target, "other": other_target}
            messages.success(request, message % targets_names)
