from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from ....acl.admin.forms import get_permissions_forms
from ....acl.admin.views import RoleAdmin, RolesList
from ....acl.cache import clear_acl_cache
from ....acl.models import Role
from ....admin.views import generic
from ...models import Category, CategoryRole, RoleCategoryACL
from ..forms import (
    CategoryRoleForm,
    CategoryRolesACLFormFactory,
    RoleCategoryACLFormFactory,
)
from .categories import CategoriesList, CategoryAdmin


class CategoryRoleAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:permissions:categories:index"
    model = CategoryRole
    templates_dir = "misago/admin/categoryroles"
    message_404 = _("Requested role does not exist.")


class CategoryRolesList(CategoryRoleAdmin, generic.ListView):
    ordering = (("name", None),)


class RoleFormMixin:
    def real_dispatch(self, request, target):
        form = CategoryRoleForm(instance=target)

        perms_forms = get_permissions_forms(target)

        if request.method == "POST":
            perms_forms = get_permissions_forms(target, request.POST)
            valid_forms = 0
            for permissions_form in perms_forms:
                if permissions_form.is_valid():
                    valid_forms += 1

            form = CategoryRoleForm(request.POST, instance=target)
            if form.is_valid():
                if len(perms_forms) == valid_forms:
                    new_permissions = {}
                    for permissions_form in perms_forms:
                        cleaned_data = permissions_form.cleaned_data
                        new_permissions[permissions_form.prefix] = cleaned_data

                    form.instance.permissions = new_permissions
                    form.instance.save()

                    messages.success(
                        request, self.message_submit % {"name": target.name}
                    )

                    if "stay" in request.POST:
                        return redirect(request.path)
                    return redirect(self.root_link)

                form.add_error(None, _("Form contains errors."))

        template_name = self.get_template_name(request, target)
        return self.render(
            request,
            {"form": form, "target": target, "perms_forms": perms_forms},
            template_name,
        )


class NewCategoryRole(RoleFormMixin, CategoryRoleAdmin, generic.ModelFormView):
    message_submit = _('New role "%(name)s" has been saved.')


class EditCategoryRole(RoleFormMixin, CategoryRoleAdmin, generic.ModelFormView):
    message_submit = _('Role "%(name)s" has been changed.')


class DeleteCategoryRole(CategoryRoleAdmin, generic.ButtonView):
    def check_permissions(self, request, target):
        if target.special_role:
            message = _('Role "%(name)s" is special role and can\'t be deleted.')
            return message % {"name": target.name}

    def button_action(self, request, target):
        target.delete()
        message = _('Role "%(name)s" has been deleted.')
        messages.success(request, message % {"name": target.name})


class CategoryPermissions(CategoryAdmin, generic.ModelFormView):
    templates_dir = "misago/admin/categoryroles"
    template_name = "categoryroles.html"

    def real_dispatch(self, request, target):
        category_roles = CategoryRole.objects.order_by("name")

        assigned_roles = {}
        for acl in target.category_role_set.select_related("category_role"):
            assigned_roles[acl.role_id] = acl.category_role

        forms = []
        forms_are_valid = True
        for role in Role.objects.order_by("name"):
            FormType = CategoryRolesACLFormFactory(
                role, category_roles, assigned_roles.get(role.pk)
            )

            if request.method == "POST":
                forms.append(FormType(request.POST, prefix=role.pk))
                if not forms[-1].is_valid():
                    forms_are_valid = False
            else:
                forms.append(FormType(prefix=role.pk))

        if request.method == "POST" and forms_are_valid:
            target.category_role_set.all().delete()
            new_permissions = []
            for form in forms:
                if form.cleaned_data["category_role"]:
                    new_permissions.append(
                        RoleCategoryACL(
                            role=form.role,
                            category=target,
                            category_role=form.cleaned_data["category_role"],
                        )
                    )
            if new_permissions:
                RoleCategoryACL.objects.bulk_create(new_permissions)

            clear_acl_cache()

            message = _("Category %(name)s permissions have been changed.")
            messages.success(request, message % {"name": target.name})
            if "stay" in request.POST:
                return redirect(request.path)
            return redirect(self.root_link)

        template_name = self.get_template_name(request, target)
        return self.render(request, {"forms": forms, "target": target}, template_name)


CategoriesList.add_item_action(
    name=_("Change permissions"), link="misago:admin:categories:permissions"
)


class RoleCategoriesACL(RoleAdmin, generic.ModelFormView):
    templates_dir = "misago/admin/categoryroles"
    template_name = "rolecategories.html"

    def real_dispatch(self, request, target):
        categories = Category.objects.all_categories()
        roles = CategoryRole.objects.order_by("name")

        if not categories:
            messages.info(request, _("No categories exist."))
            return redirect(self.root_link)

        choices = {}
        for choice in target.categories_acls.select_related("category_role"):
            choices[choice.category_id] = choice.category_role

        forms = []
        forms_are_valid = True
        for category in categories:
            category.level_range = range(category.level - 1)
            FormType = RoleCategoryACLFormFactory(
                category, roles, choices.get(category.pk)
            )

            if request.method == "POST":
                forms.append(FormType(request.POST, prefix=category.pk))
                if not forms[-1].is_valid():
                    forms_are_valid = False
            else:
                forms.append(FormType(prefix=category.pk))

        if request.method == "POST" and forms_are_valid:
            target.categories_acls.all().delete()
            new_permissions = []
            for form in forms:
                if form.cleaned_data["role"]:
                    new_permissions.append(
                        RoleCategoryACL(
                            role=target,
                            category=form.category,
                            category_role=form.cleaned_data["role"],
                        )
                    )
            if new_permissions:
                RoleCategoryACL.objects.bulk_create(new_permissions)

            clear_acl_cache()

            message = _("Category permissions for role %(name)s have been changed.")
            messages.success(request, message % {"name": target.name})
            if "stay" in request.POST:
                return redirect(request.path)
            return redirect(self.root_link)

        template_name = self.get_template_name(request, target)
        return self.render(request, {"forms": forms, "target": target}, template_name)


RolesList.add_item_action(
    name=_("Categories permissions"), link="misago:admin:permissions:categories"
)
