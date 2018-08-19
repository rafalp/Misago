from mptt.forms import TreeNodeChoiceField, TreeNodeMultipleChoiceField

from django import forms
from django.db import models
from django.utils.html import conditional_escape, mark_safe
from django.utils.translation import ugettext_lazy as _

from misago.core.forms import YesNoSwitch
from misago.core.validators import validate_sluggable
from misago.threads.threadtypes import trees_map

from . import THREADS_ROOT_NAME
from .models import Category, CategoryRole


class AdminCategoryFieldMixin(object):
    def __init__(self, *args, **kwargs):
        self.base_level = kwargs.pop('base_level', 1)
        kwargs['level_indicator'] = kwargs.get('level_indicator', '- - ')

        threads_tree_id = trees_map.get_tree_id_for_root(THREADS_ROOT_NAME)
        queryset = Category.objects.filter(tree_id=threads_tree_id)
        if not kwargs.pop('include_root', False):
            queryset = queryset.exclude(special_role="root_category")

        kwargs.setdefault('queryset', queryset)

        super(AdminCategoryFieldMixin, self).__init__(*args, **kwargs)

    def _get_level_indicator(self, obj):
        level = getattr(obj, obj._mptt_meta.level_attr) - self.base_level
        if level > 0:
            return mark_safe(conditional_escape(self.level_indicator) * level)
        else:
            return ''


class AdminCategoryChoiceField(AdminCategoryFieldMixin, TreeNodeChoiceField):
    pass


class AdminCategoryMultipleChoiceField(AdminCategoryFieldMixin, TreeNodeMultipleChoiceField):
    pass


class CategoryFormBase(forms.ModelForm):
    name = forms.CharField(label=_("Name"), validators=[validate_sluggable()])
    description = forms.CharField(
        label=_("Description"),
        max_length=2048,
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text=_("Optional description explaining category intented purpose."),
    )
    css_class = forms.CharField(
        label=_("CSS class"),
        required=False,
        help_text=_(
            "Optional CSS class used to customize this category appearance from templates."
        ),
    )
    is_closed = YesNoSwitch(
        label=_("Closed category"),
        required=False,
        help_text=_("Only members with valid permissions can post in closed categories."),
    )
    css_class = forms.CharField(
        label=_("CSS class"),
        required=False,
        help_text=_(
            "Optional CSS class used to customize this category appearance from templates."
        ),
    )
    require_threads_approval = YesNoSwitch(
        label=_("Threads"),
        required=False,
        help_text=_("All threads started in this category will require moderator approval."),
    )
    require_replies_approval = YesNoSwitch(
        label=_("Replies"),
        required=False,
        help_text=_("All replies posted in this category will require moderator approval."),
    )
    require_edits_approval = YesNoSwitch(
        label=_("Edits"),
        required=False,
        help_text=_(
            "Will make all edited replies return to unapproved state for moderator to review."
        ),
    )
    prune_started_after = forms.IntegerField(
        label=_("Thread age"),
        min_value=0,
        help_text=_(
            "Prune thread if number of days since its creation is greater than specified. "
            "Enter 0 to disable this pruning criteria."
        ),
    )
    prune_replied_after = forms.IntegerField(
        label=_("Last reply"),
        min_value=0,
        help_text=_(
            "Prune thread if number of days since last reply is greater than specified. "
            "Enter 0 to disable this pruning criteria."
        ),
    )

    class Meta:
        model = Category
        fields = [
            'name',
            'description',
            'css_class',
            'is_closed',
            'require_threads_approval',
            'require_replies_approval',
            'require_edits_approval',
            'prune_started_after',
            'prune_replied_after',
            'archive_pruned_in',
        ]

    def clean_copy_permissions(self):
        data = self.cleaned_data['copy_permissions']
        if data and data.pk == self.instance.pk:
            message = _("Permissions cannot be copied from category into itself.")
            raise forms.ValidationError(message)
        return data

    def clean_archive_pruned_in(self):
        data = self.cleaned_data['archive_pruned_in']
        if data and data.pk == self.instance.pk:
            message = _("Category cannot act as archive for itself.")
            raise forms.ValidationError(message)
        return data

    def clean(self):
        data = super(CategoryFormBase, self).clean()
        self.instance.set_name(data.get('name'))
        return data


def CategoryFormFactory(instance):
    parent_queryset = Category.objects.all_categories(True).order_by('lft')
    if instance.pk:
        not_siblings = models.Q(lft__lt=instance.lft)
        not_siblings = not_siblings | models.Q(rght__gt=instance.rght)
        parent_queryset = parent_queryset.filter(not_siblings)

    return type(
        'CategoryFormFinal', (CategoryFormBase, ), {
            'new_parent': AdminCategoryChoiceField(
                label=_("Parent category"),
                queryset=parent_queryset,
                initial=instance.parent,
                empty_label=None,
            ),
            'copy_permissions': AdminCategoryChoiceField(
                label=_("Copy permissions"),
                help_text=_(
                    "You can replace this category permissions with "
                    "permissions copied from category selected here."
                ),
                queryset=Category.objects.all_categories(),
                empty_label=_("Don't copy permissions"),
                required=False,
            ),
            'archive_pruned_in': AdminCategoryChoiceField(
                label=_("Archive"),
                help_text=_(
                    "Instead of being deleted, pruned threads can be "
                    "moved to designated category."
                ),
                queryset=Category.objects.all_categories(),
                empty_label=_("Don't archive pruned threads"),
                required=False,
            ),
        }
    )


class DeleteCategoryFormBase(forms.ModelForm):
    class Meta:
        model = Category
        fields = []

    def clean(self):
        data = super(DeleteCategoryFormBase, self).clean()

        if data.get('move_threads_to'):
            if data['move_threads_to'].pk == self.instance.pk:
                message = _("You are trying to move this category threads to itself.")
                raise forms.ValidationError(message)

            moving_to_child = self.instance.has_child(data['move_threads_to'])
            if moving_to_child and not data.get('move_children_to'):
                message = _(
                    "You are trying to move this category threads to a "
                    "child category that will be deleted together with "
                    "this category."
                )
                raise forms.ValidationError(message)

        return data


def DeleteFormFactory(instance):
    content_queryset = Category.objects.all_categories().order_by('lft')
    fields = {
        'move_threads_to': AdminCategoryChoiceField(
            label=_("Move category threads to"),
            queryset=content_queryset,
            initial=instance.parent,
            empty_label=_('Delete with category'),
            required=False,
        )
    }

    not_siblings = models.Q(lft__lt=instance.lft)
    not_siblings = not_siblings | models.Q(rght__gt=instance.rght)
    children_queryset = Category.objects.all_categories(True)
    children_queryset = children_queryset.filter(not_siblings).order_by('lft')

    if children_queryset.exists():
        fields['move_children_to'] = AdminCategoryChoiceField(
            label=_("Move child categories to"),
            queryset=children_queryset,
            empty_label=_('Delete with category'),
            required=False,
        )

    return type('DeleteCategoryFormFinal', (DeleteCategoryFormBase, ), fields)


class CategoryRoleForm(forms.ModelForm):
    name = forms.CharField(label=_("Role name"))

    class Meta:
        model = CategoryRole
        fields = ['name']


def RoleCategoryACLFormFactory(category, category_roles, selected_role):
    attrs = {
        'category': category,
        'role': forms.ModelChoiceField(
            label=_("Role"),
            required=False,
            queryset=category_roles,
            initial=selected_role,
            empty_label=_("No access"),
        )
    }

    return type('RoleCategoryACLForm', (forms.Form, ), attrs)


def CategoryRolesACLFormFactory(role, category_roles, selected_role):
    attrs = {
        'role': role,
        'category_role': forms.ModelChoiceField(
            label=_("Role"),
            required=False,
            queryset=category_roles,
            initial=selected_role,
            empty_label=_("No access"),
        )
    }

    return type('CategoryRolesACLForm', (forms.Form, ), attrs)
