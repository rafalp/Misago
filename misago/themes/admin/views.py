from django.contrib import messages
from django.db.models import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy as _

from ...admin.views import generic
from ..models import Theme, Css
from .css import move_css_down, move_css_up
from .forms import CssEditorForm, ThemeForm, UploadCssForm, UploadMediaForm


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
        return redirect("misago:admin:appearance:themes:assets", pk=theme.pk)


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


class ThemeCssAdmin(ThemeAssetsAdmin, generic.TargetedView):
    def wrapped_dispatch(self, request, pk, css_pk=None):
        theme = self.get_target_or_none(request, {"pk": pk})
        if not theme:
            messages.error(request, self.message_404)
            return redirect(self.root_link)

        error = self.check_permissions(  # pylint: disable=assignment-from-no-return
            request, theme
        )
        if error:
            messages.error(request, error)
            return redirect(self.root_link)

        css = self.get_theme_css_or_none(theme, css_pk)
        if css_pk and not css:
            css_error = gettext("Requested CSS could not be found in the theme.")
            messages.error(request, css_error)
            return self.redirect_to_theme_assets(theme)

        return self.real_dispatch(request, theme, css)

    def get_theme_css_or_none(self, theme, css_pk):
        if not css_pk:
            return None

        try:
            return theme.css.select_for_update().get(pk=css_pk)
        except ObjectDoesNotExist:
            return None


class MoveThemeCssUp(ThemeCssAdmin):
    def real_dispatch(self, request, theme, css):
        if request.method == "POST" and move_css_up(theme, css):
            messages.success(request, gettext('"%s" was moved up.') % css)

        return self.redirect_to_theme_assets(theme)


class MoveThemeCssDown(ThemeCssAdmin):
    def real_dispatch(self, request, theme, css):
        if request.method == "POST" and move_css_down(theme, css):
            messages.success(request, gettext('"%s" was moved down.') % css)

        return self.redirect_to_theme_assets(theme)


class ThemeCssFormAdmin(ThemeCssAdmin, generic.ModelFormView):
    def real_dispatch(self, request, theme, css=None):
        form = self.initialize_form(self.form, request, theme, css)

        if request.method == "POST" and form.is_valid():
            response = self.handle_form(  # pylint: disable=assignment-from-no-return
                form, request, theme, css
            )
            if response:
                return response
            if "stay" in request.POST:
                return self.redirect_to_edit_form(theme, form.instance)
            return self.redirect_to_theme_assets(theme)

        return self.render(request, {"form": form, "theme": theme, "target": css})

    def handle_form(self, form, request, theme, css):
        form.save()
        messages.success(request, self.message_submit % {"name": css.name})

    def redirect_to_edit_form(self, theme, css):
        return redirect(
            "misago:admin:appearance:themes:edit-css", pk=theme.pk, css_pk=css.pk
        )


class NewThemeCss(ThemeCssFormAdmin):
    message_submit = _('New CSS "%(name)s" has been saved.')
    form = CssEditorForm
    template = "assets/css-editor.html"

    def get_theme_css_or_none(self, theme, _):
        return Css(theme=theme)

    def initialize_form(self, form, request, theme, css):
        if request.method == "POST":
            return form(request.POST, instance=css)
        return form(instance=css)


class EditThemeCss(NewThemeCss):
    message_submit = _('CSS "%(name)s" has been updated.')

    def get_theme_css_or_none(self, theme, css_pk):
        try:
            return theme.css.get(pk=css_pk, url__isnull=True)
        except ObjectDoesNotExist:
            return None

    def initialize_form(self, form, request, theme, css):
        if request.method == "POST":
            return form(request.POST, instance=css)
        initial_data = {"source": css.source_file.read()}
        return form(instance=css, initial=initial_data)
