from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from ... import THREADS_ROOT_NAME
from ....acl.cache import clear_acl_cache
from ....admin.views import generic
from ....threads.threadtypes import trees_map
from ...models import Category, RoleCategoryACL
from ..forms import CategoryFormFactory, DeleteFormFactory


class CategoryAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:categories:index"
    model = Category
    templates_dir = "misago/admin/categories"
    message_404 = _("Requested category does not exist.")

    def get_target(self, kwargs):
        target = super().get_target(kwargs)

        threads_tree_id = trees_map.get_tree_id_for_root(THREADS_ROOT_NAME)

        target_is_special = bool(target.special_role)
        target_not_in_categories_tree = target.tree_id != threads_tree_id

        if target.pk and (target_is_special or target_not_in_categories_tree):
            raise Category.DoesNotExist()
        else:
            return target


class CategoriesList(CategoryAdmin, generic.ListView):
    def get_queryset(self):
        return Category.objects.all_categories()

    def process_context(self, request, context):
        context["items"] = [f for f in context["items"]]

        children_lists = {}

        for item in context["items"]:
            item.level_range = range(item.level - 1)
            item.first = False
            item.last = False
            children_lists.setdefault(item.parent_id, []).append(item)

        for level_items in children_lists.values():
            level_items[0].first = True
            level_items[-1].last = True

        return context


class CategoryFormMixin:
    def get_form_class(self, request, target):
        return CategoryFormFactory(target)

    def handle_form(self, form, request, target):
        if form.instance.pk:
            if form.instance.parent_id != form.cleaned_data["new_parent"].pk:
                form.instance.move_to(
                    form.cleaned_data["new_parent"], position="last-child"
                )
            form.instance.save()
            if form.instance.parent_id != form.cleaned_data["new_parent"].pk:
                Category.objects.clear_cache()
        else:
            form.instance.insert_at(
                form.cleaned_data["new_parent"], position="last-child", save=True
            )
            Category.objects.clear_cache()

        if form.cleaned_data.get("copy_permissions"):
            form.instance.category_role_set.all().delete()
            copy_from = form.cleaned_data["copy_permissions"]

            copied_acls = []
            for acl in copy_from.category_role_set.all():
                copied_acls.append(
                    RoleCategoryACL(
                        role_id=acl.role_id,
                        category=form.instance,
                        category_role_id=acl.category_role_id,
                    )
                )

            if copied_acls:
                RoleCategoryACL.objects.bulk_create(copied_acls)

        clear_acl_cache()
        messages.success(request, self.message_submit % {"name": target.name})


class NewCategory(CategoryFormMixin, CategoryAdmin, generic.ModelFormView):
    message_submit = _('New category "%(name)s" has been saved.')


class EditCategory(CategoryFormMixin, CategoryAdmin, generic.ModelFormView):
    message_submit = _('Category "%(name)s" has been edited.')


class DeleteCategory(CategoryAdmin, generic.ModelFormView):
    message_submit = _('Category "%(name)s" has been deleted.')
    template_name = "delete.html"

    def get_form_class(self, request, target):
        return DeleteFormFactory(target)

    def handle_form(self, form, request, target):
        move_children_to = form.cleaned_data.get("move_children_to")
        move_threads_to = form.cleaned_data.get("move_threads_to")

        if move_children_to:
            for child in target.get_children():
                # refresh child and new parent
                move_children_to = Category.objects.get(pk=move_children_to.pk)
                child = Category.objects.get(pk=child.pk)

                child.move_to(move_children_to, "last-child")
                if move_threads_to and child.pk == move_threads_to.pk:
                    move_threads_to = child
        else:
            for child in target.get_descendants().order_by("-lft"):
                child.delete_content()
                child.delete()

        if move_threads_to:
            target.move_content(move_threads_to)
            move_threads_to.synchronize()
            move_threads_to.save()
        else:
            target.delete_content()

        # refresh instance
        instance = Category.objects.get(pk=form.instance.pk)
        instance.delete()

        messages.success(request, self.message_submit % {"name": target.name})
        return redirect(self.root_link)


class MoveDownCategory(CategoryAdmin, generic.ButtonView):
    def button_action(self, request, target):
        try:
            other_target = target.get_next_sibling()
        except Category.DoesNotExist:
            other_target = None

        if other_target:
            Category.objects.move_node(target, other_target, "right")
            Category.objects.clear_cache()

            message = _('Category "%(name)s" has been moved below "%(other)s".')
            targets_names = {"name": target.name, "other": other_target.name}
            messages.success(request, message % targets_names)


class MoveUpCategory(CategoryAdmin, generic.ButtonView):
    def button_action(self, request, target):
        try:
            other_target = target.get_previous_sibling()
        except Category.DoesNotExist:
            other_target = None

        if other_target:
            Category.objects.move_node(target, other_target, "left")
            Category.objects.clear_cache()

            message = _('Category "%(name)s" has been moved above "%(other)s".')
            targets_names = {"name": target.name, "other": other_target.name}
            messages.success(request, message % targets_names)
