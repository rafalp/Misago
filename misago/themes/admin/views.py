from django.contrib import messages
from django.db.models import ObjectDoesNotExist
from django.shortcuts import redirect
from django.utils.translation import gettext, gettext_lazy as _

from ...admin.views import generic
from ..cache import clear_theme_cache
from ..models import Theme, Css
from .css import move_css_down, move_css_up
from .exporter import export_theme
from .forms import (
    CssEditorForm,
    CssLinkForm,
    ImportForm,
    ThemeForm,
    UploadCssForm,
    UploadMediaForm,
)
from .importer import ThemeImportError, import_theme
from .tasks import build_single_theme_css, build_theme_css, update_remote_css_size


class ThemeAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:themes:index"
    model = Theme
    form_class = ThemeForm
    templates_dir = "misago/admin/themes"
    message_404 = _("Requested theme does not exist.")


class ThemesList(ThemeAdmin, generic.ListView):
    pass


class NewTheme(ThemeAdmin, generic.ModelFormView):
    message_submit = _('New theme "%(name)s" has been saved.')

    def get_form(self, form_class, request, _):
        if request.method == "POST":
            return form_class(request.POST, request.FILES)

        try:
            initial = {"parent": int(request.GET.get("parent"))}
        except (TypeError, ValueError):
            initial = {}

        return form_class(initial=initial)


class EditTheme(ThemeAdmin, generic.ModelFormView):
    message_submit = _('Theme "%(name)s" has been updated.')

    def check_permissions(self, request, target):
        if target.is_default:
            return gettext("Default theme can't be edited.")

    def handle_form(self, form, request, target):
        super().handle_form(form, request, target)
        if "parent" in form.changed_data:
            clear_theme_cache()


class DeleteTheme(ThemeAdmin, generic.ButtonView):
    message_submit = _('Theme "%(name)s" has been deleted.')

    def check_permissions(self, request, target):
        if target.is_default:
            return gettext("Default theme can't be deleted.")
        if target.is_active:
            return gettext("Active theme can't be deleted.")
        if target.get_descendants().filter(is_active=True).exists():
            message = gettext(
                'Theme "%(name)s" can\'t be deleted '
                "because one of its child themes is set as active."
            )
            return message % {"name": target}

    def button_action(self, request, target):
        for theme in reversed(target.get_descendants(include_self=True)):
            theme.delete()

        clear_theme_cache()
        messages.success(request, self.message_submit % {"name": target})


class ActivateTheme(ThemeAdmin, generic.ButtonView):
    def button_action(self, request, target):
        set_theme_as_active(request, target)

        message = gettext('Active theme has been changed to "%(name)s".')
        messages.success(request, message % {"name": target})


def set_theme_as_active(request, theme):
    Theme.objects.update(is_active=False)
    Theme.objects.filter(pk=theme.pk).update(is_active=True)
    clear_theme_cache()


class ExportTheme(ThemeAdmin, generic.ButtonView):
    def check_permissions(self, request, target):
        if target.is_default:
            return gettext("Default theme can't be exported.")

    def button_action(self, request, target):
        return export_theme(target)


class ImportTheme(ThemeAdmin, generic.FormView):
    form_class = ImportForm
    template_name = "import.html"

    def handle_form(self, form, request):
        try:
            self.import_theme(request, **form.cleaned_data)
            return redirect(self.root_link)
        except ThemeImportError as e:
            form.add_error("upload", str(e))
            return self.render(request, {"form": form})

    def import_theme(self, request, *_, name, parent, upload):
        theme = import_theme(name, parent, upload)
        message = gettext('Theme "%(name)s" has been imported.')
        messages.success(request, message % {"name": theme})


class ThemeAssetsAdmin(ThemeAdmin):
    def check_permissions(self, request, theme):
        if theme.is_default:
            return gettext("Default theme assets can't be edited.")

    def redirect_to_theme_assets(self, theme):
        return redirect("misago:admin:themes:assets", pk=theme.pk)


class ThemeAssets(ThemeAssetsAdmin, generic.TargetedView):
    template_name = "assets/list.html"

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
    form_class = None

    def action(self, request, theme):
        form = self.form_class(  # pylint: disable=not-callable
            request.POST, request.FILES, instance=theme
        )

        if not form.is_valid():
            if form.cleaned_data.get("assets"):
                messages.info(request, self.message_partial_success)
            for error in form.errors["assets"]:
                messages.error(request, error)

        if form.cleaned_data.get("assets"):
            form.save()
            build_theme_css.delay(theme.pk)
            messages.success(request, self.message_success)


class UploadThemeCss(UploadThemeAssets):
    message_success = _("New CSS files have been added to the theme.")
    form_class = UploadCssForm


class UploadThemeMedia(UploadThemeAssets):
    message_success = _("New media files have been added to the theme.")
    form_class = UploadMediaForm


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

    def action(self, request, theme):
        super().action(request, theme)
        clear_theme_cache()


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

    def real_dispatch(self, request, theme, css):
        raise NotImplementedError(
            "Admin views extending the ThemeCssAdmin"
            "should define real_dispatch(request, theme, css)"
        )


class MoveThemeCssUp(ThemeCssAdmin):
    def real_dispatch(self, request, theme, css):
        if request.method == "POST" and move_css_up(theme, css):
            clear_theme_cache()
            messages.success(request, gettext('"%s" was moved up.') % css)

        return self.redirect_to_theme_assets(theme)


class MoveThemeCssDown(ThemeCssAdmin):
    def real_dispatch(self, request, theme, css):
        if request.method == "POST" and move_css_down(theme, css):
            clear_theme_cache()
            messages.success(request, gettext('"%s" was moved down.') % css)

        return self.redirect_to_theme_assets(theme)


class ThemeCssFormAdmin(ThemeCssAdmin, generic.ModelFormView):
    is_atomic = False  # atomic updates cause race condition with celery tasks

    def real_dispatch(self, request, theme, css=None):
        form = self.get_form(self.form_class, request, theme, css)

        if request.method == "POST" and form.is_valid():
            response = self.handle_form(  # pylint: disable=assignment-from-no-return
                form, request, theme, css
            )
            if response:
                return response
            if "stay" in request.POST:
                return self.redirect_to_edit_form(theme, form.instance)
            return self.redirect_to_theme_assets(theme)

        template_name = self.get_template_name(request, css)
        return self.render(
            request, {"form": form, "theme": theme, "target": css}, template_name
        )

    def get_form(self, form_class, request, theme, css):
        raise NotImplementedError(
            "Admin views extending the ThemeCssFormAdmin "
            "should define the get_form(form_class, request, theme, css)"
        )

    def handle_form(self, form, request, theme, css):
        form.save()
        if css.source_needs_building:
            build_single_theme_css.delay(css.pk)
        else:
            clear_theme_cache()
        messages.success(request, self.message_submit % {"name": css.name})


class NewThemeCss(ThemeCssFormAdmin):
    message_submit = _('New CSS "%(name)s" has been saved.')
    form_class = CssEditorForm
    template_name = "assets/css-editor-form.html"

    def get_theme_css_or_none(self, theme, _):
        return Css(theme=theme)

    def get_form(self, form_class, request, theme, css):
        if request.method == "POST":
            return form_class(request.POST, instance=css)
        return form_class(instance=css)

    def redirect_to_edit_form(self, theme, css):
        return redirect("misago:admin:themes:edit-css-file", pk=theme.pk, css_pk=css.pk)


class EditThemeCss(NewThemeCss):
    message_submit = _('CSS "%(name)s" has been updated.')

    def get_theme_css_or_none(self, theme, css_pk):
        try:
            return theme.css.get(pk=css_pk, url__isnull=True)
        except ObjectDoesNotExist:
            return None

    def get_form(self, form_class, request, theme, css):
        if request.method == "POST":
            return form_class(request.POST, instance=css)
        initial_data = {"source": css.source_file.read().decode("utf-8")}
        return form_class(instance=css, initial=initial_data)

    def handle_form(self, form, request, theme, css):
        if "source" in form.changed_data:
            form.save()
            if css.source_needs_building:
                build_single_theme_css.delay(css.pk)
            else:
                clear_theme_cache()
            messages.success(request, self.message_submit % {"name": css.name})
        else:
            message = gettext('No changes have been made to "%(css)s".')
            messages.info(request, message % {"name": css.name})


class NewThemeCssLink(ThemeCssFormAdmin):
    message_submit = _('New CSS link "%(name)s" has been saved.')
    form_class = CssLinkForm
    template_name = "assets/css-link-form.html"

    def get_theme_css_or_none(self, theme, _):
        return Css(theme=theme)

    def get_form(self, form_class, request, theme, css):
        if request.method == "POST":
            return form_class(request.POST, instance=css)
        return form_class(instance=css)

    def handle_form(self, form, request, theme, css):
        super().handle_form(form, request, theme, css)
        if "url" in form.changed_data:
            update_remote_css_size.delay(css.pk)
            clear_theme_cache()

    def redirect_to_edit_form(self, theme, css):
        return redirect("misago:admin:themes:new-css-link", pk=theme.pk)


class EditThemeCssLink(NewThemeCssLink):
    message_submit = _('CSS link "%(name)s" has been updated.')

    def get_theme_css_or_none(self, theme, css_pk):
        try:
            return theme.css.get(pk=css_pk, url__isnull=False)
        except ObjectDoesNotExist:
            return None

    def redirect_to_edit_form(self, theme, css):
        return redirect("misago:admin:themes:edit-css-link", pk=theme.pk, css_pk=css.pk)
