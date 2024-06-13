from django import forms
from django.utils.translation import pgettext_lazy

from ..models import CategoryRole


class CategoryRoleForm(forms.ModelForm):
    name = forms.CharField(label=pgettext_lazy("admin category role form", "Role name"))

    class Meta:
        model = CategoryRole
        fields = ["name"]


def RoleCategoryACLFormFactory(category, category_roles, selected_role):
    attrs = {
        "category": category,
        "role": forms.ModelChoiceField(
            label=pgettext_lazy("admin permissions form", "Role"),
            required=False,
            queryset=category_roles,
            initial=selected_role,
            empty_label=pgettext_lazy("admin permissions form", "No access"),
        ),
    }

    return type("RoleCategoryACLForm", (forms.Form,), attrs)


def CategoryRolesACLFormFactory(role, category_roles, selected_role):
    attrs = {
        "role": role,
        "category_role": forms.ModelChoiceField(
            label=pgettext_lazy("admin permissions form", "Role"),
            required=False,
            queryset=category_roles,
            initial=selected_role,
            empty_label=pgettext_lazy("admin permissions form", "No access"),
        ),
    }

    return type("CategoryRolesACLForm", (forms.Form,), attrs)
