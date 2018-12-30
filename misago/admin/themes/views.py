from django.contrib import messages
from django.db.models import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy as _

from ...themes.models import Theme
from ..views import generic
from .forms import ThemeForm, UploadCssForm, UploadMediaForm


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


def set_theme_as_active(request, theme):
    Theme.objects.update(is_active=False)
    Theme.objects.filter(pk=theme.pk).update(is_active=True)


class ThemeAssetsAdmin(ThemeAdmin):
    def check_permissions(self, request, theme):
        if theme.is_default:
            return gettext("Default theme assets can't be edited.")

    def redirect_to_theme_assets(self, theme):
        link = reverse("misago:admin:appearance:themes:assets", kwargs={"pk": theme.pk})
        return redirect(link)


class ThemeAssets(ThemeAssetsAdmin, generic.TargetedView):
    template = "assets/list.html"

    def real_dispatch(self, request, theme):
        return self.render(request, {"theme": theme})


class ThemeAssetsActionAdmin(ThemeAssetsAdmin):
    def real_dispatch(self, request, theme):
        if request.method == "POST":
            self.action(request, theme)

        return self.redirect_to_theme_assets(theme)

    def action(self, request, theme):
        raise NotImplementedError(
            "action method must be implemented in inheriting class"
        )


class UploadThemeAssets(ThemeAssetsActionAdmin, generic.TargetedView):
    message_partial_success = _(
        "Some css files could not have been added to the theme."
    )

    message_submit = None
    form = None

    def action(self, request, theme):
        form = self.form(  # pylint: disable=not-callable
            request.POST, request.FILES, instance=theme
        )

        if not form.is_valid():
            if form.cleaned_data.get("assets"):
                messages.info(request, self.message_partial_success)
            for error in form.errors["assets"]:
                messages.error(request, error)

        if form.cleaned_data.get("assets"):
            form.save()
            messages.success(request, self.message_success)


class UploadThemeCss(UploadThemeAssets):
    message_success = _("New CSS files have been added to the theme.")
    form = UploadCssForm


class UploadThemeMedia(UploadThemeAssets):
    message_success = _("New media files have been added to the theme.")
    form = UploadMediaForm


class DeleteThemeAssets(ThemeAssetsActionAdmin, generic.TargetedView):
    message_submit = None
    queryset_attr = None

    def action(self, request, theme):
        items = self.clean_items_list(request)
        if items:
            queryset = getattr(theme, self.queryset_attr)
            for item in items:
                self.delete_asset(queryset, item)

            messages.success(request, self.message_submit)

    def clean_items_list(self, request):
        try:
            return {int(i) for i in request.POST.getlist("item")[:20]}
        except (ValueError, TypeError):
            pass

    def delete_asset(self, queryset, item):
        try:
            queryset.get(pk=item).delete()
        except ObjectDoesNotExist:
            pass


class DeleteThemeCss(DeleteThemeAssets):
    message_submit = _("Selected CSS files have been deleted.")
    queryset_attr = "css"


class DeleteThemeMedia(DeleteThemeAssets):
    message_submit = _("Selected media have been deleted.")
    queryset_attr = "media"
