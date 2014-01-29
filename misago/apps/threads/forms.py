from django.utils.translation import ungettext, ugettext_lazy as _
import floppyforms as forms
from misago.apps.threadtype.posting.forms import NewThreadForm as NewThreadFormBase, EditThreadForm as EditThreadFormBase
from misago.forms import Form
from misago.models import ThreadPrefix
from misago.validators import validate_sluggable

class PollFormMixin(object):
    def create_poll_form(self):
        self.add_field('poll_question',
                       forms.CharField(label=_("Poll Question"),
                                       required=False))
        self.add_field('poll_choices',
                       forms.CharField(label=_("Poll Choices"),
                                       help_text=_("Enter options poll members will vote on, every one in new line."),
                                       required=False,
                                       widget=forms.Textarea))
        self.add_field('poll_max_choices',
                       forms.IntegerField(label=_("Choices Per User"),
                                          help_text=_("Select on how many options individual user will be able to vote on."),
                                          min_value=1,
                                          initial=1))
        self.add_field('poll_length',
                       forms.IntegerField(label=_("Poll Length"),
                                          help_text=_("Number of days since poll creations users will be allowed to vote in poll. Enter zero for permanent poll."),
                                          min_value=0,
                                          initial=0))
        self.add_field('poll_public',
                       forms.BooleanField(label=_("Public Voting"),
                                          required=False))
        self.add_field('poll_changing_votes',
                       forms.BooleanField(label=_("Allow Changing Votes"),
                                          required=False))

    def edit_poll_form(self):
        self.add_field('poll_question',
                       forms.CharField(label=_("Poll Question"),
                                       initial=self.poll.question))
        self.add_field('poll_choices',
                       forms.CharField(label=_("Add New Choices"),
                                       help_text=_("If you want, you can add new options to poll. Enter every option in new line."),
                                       required=False,
                                       widget=forms.Textarea))
        self.add_field('poll_max_choices',
                       forms.IntegerField(label=_("Choices Per User"),
                                          help_text=_("Select on how many options individual user will be able to vote on."),
                                          min_value=1,
                                          initial=self.poll.max_choices))
        self.add_field('poll_length',
                       forms.IntegerField(label=_("Poll Length"),
                                          help_text=_("Number of days since poll creations users will be allowed to vote in poll. Enter zero for permanent poll."),
                                          min_value=0,
                                          initial=self.poll.length))

        self.add_field('poll_changing_votes',
                       forms.BooleanField(label=_("Allow Changing Votes"),
                                          required=False,
                                          initial=self.poll.vote_changing))

    def clean_poll_question(self):
        data = self.cleaned_data['poll_question'].strip()
        if data or self.poll:
            if len(data) < 3:
                raise forms.ValidationError(_("Poll quesiton should be at least three characters long."))
            if len(data) > 255:
                raise forms.ValidationError(_("Poll quesiton should be no longer than 250 characters."))
        return data

    def clean_poll_choices(self):
        self.clean_choices = []
        self.new_choices = []
        data = self.cleaned_data['poll_choices']

        if self.poll:
            self.clean_poll_edited_choices()

        if data:
            for choice in data.splitlines():
                choice = choice.strip()
                if not choice in self.clean_choices:
                    if len(choice) < 2:
                        raise forms.ValidationError(_("Poll choices should be at least two characters long."))
                    if len(choice) > 250:
                        raise forms.ValidationError(_("Poll choices should be no longer than 250 characters."))
                    self.clean_choices.append(choice)
                    self.new_choices.append(choice)
            if len(self.clean_choices) < 2:
                raise forms.ValidationError(_("Poll needs at least two choices."))
            if len(self.clean_choices) > 10:
                raise forms.ValidationError(_("Poll cannot have more than 10 choices."))

        return '\r\n'.join(self.clean_choices)

    def clean_poll_edited_choices(self):
        self.changed_choices = []
        self.deleted_choices = []

        for option in self.poll.option_set.all():
            new_name = self.request.POST.get('poll_current_choices[%s]' % option.pk, u'')
            new_name = new_name.strip()
            if new_name:
                self.clean_choices.append(new_name)
                if new_name != option.name:
                    option.name = new_name
                    self.changed_choices.append(option)
            else:
                self.deleted_choices.append(option)

    def clean_poll_max_choices(self):
        data = self.cleaned_data['poll_max_choices']
        if data < 1:
            raise forms.ValidationError(_("Voters must be allowed to make at least one choice."))
        if self.clean_choices and data > len(self.clean_choices):
            raise forms.ValidationError(_("Users cannot cast more votes than there are options."))
        return data

    def clean_poll_length(self):
        data = self.cleaned_data['poll_length']
        if data < 0:
            raise forms.ValidationError(_("Poll length cannot be negative."))
        if data > 300:
            raise forms.ValidationError(_("Poll length cannot be longer than 300 days."))
        if self.poll:
            org_length = self.poll.length
            self.poll.length = data
            try:
                if self.poll.over:
                    raise forms.ValidationError(_("You cannot close poll that way."))
            finally:
                org_length = self.poll.length
                self.poll.length = org_length
        return data

    def clean_poll(self, data):
        try:
            if bool(data['poll_question']) != bool(self.clean_choices):
                if bool(data['poll_question']):
                    raise forms.ValidationError(_("You have to define poll choices."))
                else:
                    raise forms.ValidationError(_("You have to define poll question."))
        except KeyError:
            pass
        return data


class ThreadPrefixMixin(object):
    def create_prefix_form(self):
        self.prefixes = ThreadPrefix.objects.forum_prefixes(self.forum)
        if self.prefixes:
            self.add_field('thread_prefix',
                           forms.TypedChoiceField(label=_("Thread Prefix"),
                                                  choices=[(0, _("No prefix"))] + [(p.pk, _(p.name)) for p in self.prefixes.values()],
                                                  coerce=int, required=False, empty_value=0, initial=self.thread.prefix_id if self.thread else None))


class NewThreadForm(NewThreadFormBase, PollFormMixin, ThreadPrefixMixin):
    def type_fields(self):
        self.poll = None
        if self.request.acl.threads.can_make_polls(self.forum):
            self.create_poll_form()

        if self.request.acl.threads.can_change_prefix(self.forum):
            self.create_prefix_form()

    def clean(self):
        data = super(NewThreadForm, self).clean()
        data = self.clean_poll(data)
        return data


class EditThreadForm(EditThreadFormBase, PollFormMixin, ThreadPrefixMixin):
    def type_fields(self):
        self.poll = self.thread.poll

        if self.poll:
            if self.request.acl.threads.can_edit_poll(self.forum, self.poll):
                self.edit_poll_form()
        else:
            if self.request.acl.threads.can_make_polls(self.forum):
                self.create_poll_form()

        if self.poll and self.request.acl.threads.can_delete_poll(self.forum, self.poll):
            self.add_field('poll_delete',
                           forms.BooleanField(label=_("Delete poll"),
                                              required=False))

        if self.request.acl.threads.can_change_prefix(self.forum):
            self.create_prefix_form()

    def clean(self):
        data = super(EditThreadForm, self).clean()
        data = self.clean_poll(data)
        return data


class PollVoteForm(Form):
    def __init__(self, *args, **kwargs):
        self.poll = kwargs.pop('poll')
        super(PollVoteForm, self).__init__(*args, **kwargs)

    def finalize_form(self):
        choices = []
        for choice in self.poll.choices_cache:
            choices.append((choice['pk'], choice['name']))
        if self.poll.max_choices > 1:
            self.add_field('options',
                           forms.TypedMultipleChoiceField(choices=choices, coerce=int, required=False,
                                                          widget=forms.CheckboxSelectMultiple))
        else:
            self.add_field('options',
                           forms.TypedChoiceField(choices=choices, coerce=int, required=False,
                                                  widget=forms.RadioSelect))

    def clean_options(self):
        data = self.cleaned_data['options']
        try:
            if not data:
                raise forms.ValidationError(_("You have to make selection."))
            if len(data) > self.poll.max_choices:
                raise forms.ValidationError(ungettext("You cannot select more than one option.",
                                                      "You cannot select more than %(limit)s options.",
                                                      self.poll.max_choices) % {'limit': self.poll.max_choices})
        except TypeError:
            pass
        return data
