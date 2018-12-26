from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy as _

from ...theming.models import Theme
from ..views import generic
from .forms import ThemeForm


class ThemeAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:appearance:themes:index"
    model = Theme
    form = ThemeForm
    templates_dir = "misago/admin/themes"
    message_404 = _("Requested theme does not exist.")


class ThemesList(ThemeAdmin, generic.ListView):
    pass


class NewTheme(ThemeAdmin, generic.ModelFormView):
    message_submit = _('New theme "%(name)s" has been saved.')

    def initialize_form(self, form, request, _):
        if request.method == "POST":
            return form(request.POST, request.FILES)

        try:
            initial = {"parent": int(request.GET.get("parent"))}
        except (TypeError, ValueError):
            initial = {}

        return form(initial=initial)


class EditTheme(ThemeAdmin, generic.ModelFormView):
    message_submit = _('Theme "%(name)s" has been updated.')

    def check_permissions(self, request, target):
        if target.is_default:
            return gettext("Default theme can't be edited.")


class DeleteTheme(ThemeAdmin, generic.ModelFormView):
    message_submit = _('Theme "%(name)s" has been deleted.')

    def check_permissions(self, request, target):
        if target.is_default:
            return gettext("Default theme can't be deleted.")


class ActivateTheme(ThemeAdmin, generic.ButtonView):
    def button_action(self, request, target):
        set_theme_as_active(request, target)

        message = gettext('Active theme has been changed to "%(name)s".')
        messages.success(request, message % {"name": target})


class ThemeAssets(ThemeAdmin, generic.TargetedView):
    template = "assets.html"

    def check_permissions(self, request, theme):
        if theme.is_default:
            return gettext("Default theme assets can't be edited.")

    def real_dispatch(self, request, theme):
        return self.render(request, {"theme": theme})


def set_theme_as_active(request, theme):
    Theme.objects.update(is_active=False)
    Theme.objects.filter(pk=theme.pk).update(is_active=True)
