from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import pgettext_lazy

from ...acl.cache import clear_acl_cache
from ...admin.views import generic
from ...cache.enums import CacheName
from ...cache.versions import invalidate_cache
from ...categories.delete import delete_category
from ...categories.enums import CategoryTree
from ...categories.models import Category, RoleCategoryACL
from ...permissions.admin import get_admin_category_permissions
from ...permissions.copy import copy_category_permissions
from ...permissions.models import CategoryGroupPermission
from ...users.models import Group
from .forms import CategoryForm, DeleteCategoryForm


class CategoryAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:categories:index"
    model = Category
    templates_dir = "misago/admin/categories"
    message_404 = pgettext_lazy(
        "admin categories", "Requested category does not exist."
    )

    def get_target(self, request, kwargs):
        target = super().get_target(request, kwargs)

        target_is_special = bool(target.special_role)
        target_not_in_categories_tree = target.tree_id != CategoryTree.THREADS

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
    form_class = CategoryForm

    def handle_form(self, form, request, target):
        if form.instance.pk:
            if form.instance.parent_id != form.cleaned_data["new_parent"].pk:
                form.instance.move_to(
                    form.cleaned_data["new_parent"], position="last-child"
                )
            form.instance.save()
        else:
            form.instance.insert_at(
                form.cleaned_data["new_parent"], position="last-child", save=True
            )

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

            copy_category_permissions(
                form.cleaned_data["copy_permissions"], form.instance, request
            )

        clear_acl_cache()
        invalidate_cache(
            CacheName.CATEGORIES,
            CacheName.MODERATORS,
            CacheName.PERMISSIONS,
        )

        messages.success(request, self.message_submit % {"name": target.name})


class NewCategory(CategoryFormMixin, CategoryAdmin, generic.ModelFormView):
    message_submit = pgettext_lazy(
        "admin categories", 'New category "%(name)s" has been saved.'
    )


class EditCategory(CategoryFormMixin, CategoryAdmin, generic.ModelFormView):
    message_submit = pgettext_lazy(
        "admin categories", 'Category "%(name)s" has been edited.'
    )


class CategoryPermissionsView(CategoryAdmin, generic.PermissionsFormView):
    template_name = "permissions.html"
    message_submit = pgettext_lazy(
        "admin categories", 'The "%(name)s" category permissions have been updated.'
    )

    def get_permissions(self, request, target):
        return get_admin_category_permissions(self)

    def get_items(self, request, target):
        for group in Group.objects.values("id", "name"):
            yield self.create_item(
                id=group["id"],
                name=group["name"],
            )

    def get_initial_data(self, request, target):
        return CategoryGroupPermission.objects.filter(category=target).values_list(
            "group_id", "permission"
        )

    def handle_form(self, data, request, target):
        CategoryGroupPermission.objects.filter(category=target).delete()

        new_permissions = []
        for group_id, permissions in data.items():
            for permission in permissions:
                new_permissions.append(
                    CategoryGroupPermission(
                        category=target,
                        group_id=group_id,
                        permission=permission,
                    )
                )

        if new_permissions:
            CategoryGroupPermission.objects.bulk_create(new_permissions)

        invalidate_cache(CacheName.PERMISSIONS)

        messages.success(request, self.message_submit % {"name": target.name})


class DeleteCategory(CategoryAdmin, generic.ModelFormView):
    form_class = DeleteCategoryForm
    message_submit = pgettext_lazy(
        "admin categories", 'Category "%(name)s" has been deleted.'
    )
    template_name = "delete.html"

    def handle_form(self, form, request, target):
        move_children_to = form.cleaned_data.get("move_children_to")
        move_contents_to = form.cleaned_data.get("move_contents_to")

        if move_children_to and not move_children_to.level:
            move_children_to = True

        delete_category(
            target,
            move_children_to=move_children_to,
            move_contents_to=move_contents_to,
            request=request,
        )

        invalidate_cache(
            CacheName.CATEGORIES,
            CacheName.MODERATORS,
            CacheName.PERMISSIONS,
        )

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
            invalidate_cache(CacheName.CATEGORIES)

            message = pgettext_lazy(
                "admin categories",
                'Category "%(name)s" has been moved below "%(other)s".',
            )
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
            invalidate_cache(CacheName.CATEGORIES)

            message = pgettext_lazy(
                "admin categories",
                'Category "%(name)s" has been moved above "%(other)s".',
            )
            targets_names = {"name": target.name, "other": other_target.name}
            messages.success(request, message % targets_names)
