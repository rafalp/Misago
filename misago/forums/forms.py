from django.db import models
from django.core.validators import URLValidator
from django.utils.html import conditional_escape, mark_safe
from django.utils.translation import ugettext_lazy as _
from mptt.forms import TreeNodeChoiceField as TreeNodeChoiceField
from misago.core import forms
from misago.core.validators import validate_sluggable
from misago.forums.models import Forum


class ForumChoiceField(TreeNodeChoiceField):
    def __init__(self, *args, **kwargs):
        self.base_level = kwargs.pop('base_level', 1)
        kwargs['level_indicator'] = kwargs.get('level_indicator', '- - ')
        super(ForumChoiceField, self).__init__(*args, **kwargs)

    def _get_level_indicator(self, obj):
        level = getattr(obj, obj._mptt_meta.level_attr) - self.base_level
        if level > 0:
            return mark_safe(conditional_escape(self.level_indicator) * level)
        else:
            return ''


FORUM_ROLES = (
    ('category', _('Category')),
    ('forum', _('Forum')),
    ('redirect', _('Redirect')),
)


class ForumFormBase(forms.ModelForm):
    role = forms.ChoiceField(label=_("Type"), choices=FORUM_ROLES)
    name = forms.CharField(
        label=_("Name"),
        validators=[validate_sluggable()],
        help_text=_('Short and descriptive name of all users with this rank. '
                    '"The Team" or "Game Masters" are good examples.'))
    description = forms.CharField(
        label=_("Description"), max_length=2048, required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text=_("Optional description explaining forum's intented "
                    "purpose."))
    redirect_url = forms.URLField(
        label=_("Redirect URL"),
        validators=[validate_sluggable()],
        help_text=_('If forum type is redirect, enter here its URL.'),
        required=False)
    css_class = forms.CharField(
        label=_("CSS class"), required=False,
        help_text=_("Optional CSS class used to customize this forum "
                    "appearance from templates."))
    is_closed = forms.YesNoSwitch(
        label=_("Closed forum"), required=False,
        help_text=_("Only members with valid permissions can post in "
                    "closed forums."))
    css_class = forms.CharField(
        label=_("CSS class"), required=False,
        help_text=_("Optional CSS class used to customize this forum "
                    "appearance from templates."))
    prune_started_after = forms.IntegerField(
        label=_("Prune thread if number of days since its creation is "
                "greater than"), min_value=0,
        help_text=_("Enter 0 to disable this pruning criteria."))
    prune_replied_after = forms.IntegerField(
        label=_("Prune thread if number of days since last reply is greater "
                "than"), min_value=0,
        help_text=_("Enter 0 to disable this pruning criteria."))

    class Meta:
        model = Forum
        fields = [
            'role',
            'name',
            'description',
            'redirect_url',
            'css_class',
            'is_closed',
            'prune_started_after',
            'prune_replied_after',
            'archive_pruned_in',
        ]

    def clean_copy_permissions(self):
        data = self.cleaned_data['copy_permissions']
        if data and data.pk == self.instance.pk:
            message = _("Permissions cannot be copied from forum into itself.")
            raise forms.ValidationError(message)
        return data

    def clean_archive_pruned_in(self):
        data = self.cleaned_data['archive_pruned_in']
        if data and data.pk == self.instance.pk:
            message = _("Forum cannot act as archive for itself.")
            raise forms.ValidationError(message)
        return data

    def clean(self):
        data = super(ForumFormBase, self).clean()

        self.instance.set_name(data.get('name'))
        self.instance.set_description(data.get('description'))

        if data['role'] != 'category':
            if not data['new_parent'].level:
                message = _("Only categories can have no parent category.")
                raise forms.ValidationError(message)

        if data['role'] == 'redirect':
            if not data.get('redirect'):
                message = _("This forum is redirect, yet you haven't "
                            "specified URL to which it should redirect "
                            "after click.")
                raise forms.ValidationError(message)

        return data


def ForumFormFactory(instance):
    parent_queryset = Forum.objects.all_forums(True).order_by('lft')
    if instance.pk:
        not_siblings = models.Q(lft__lt=instance.lft)
        not_siblings = not_siblings | models.Q(rght__gt=instance.rght)
        parent_queryset = parent_queryset.filter(not_siblings)

    return type('TreeNodeChoiceField', (ForumFormBase,), {
        'new_parent': ForumChoiceField(
            label=_("Parent forum"),
            queryset=parent_queryset,
            initial=instance.parent,
            empty_label=None),
        'copy_permissions': ForumChoiceField(
            label=_("Copy permissions"),
            help_text=_("You can override this forum permissions with "
                        "permissions of other forum selected here."),
            queryset=Forum.objects.all_forums(),
            empty_label=_("Don't copy permissions"),
            base_level=1,
            required=False),
        'archive_pruned_in': ForumChoiceField(
            label=_("Pruned threads archive"),
            help_text=_("Instead of being deleted, pruned threads can be "
                        "moved to designated forum."),
            queryset=Forum.objects.all_forums(),
            empty_label=_("Don't archive pruned threads"),
            base_level=1,
            required=False),
        })

