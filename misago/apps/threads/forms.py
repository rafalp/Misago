from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.apps.threadtype.posting.forms import NewThreadForm as NewThreadFormBase
from misago.forms import Form
from misago.validators import validate_sluggable

class NewThreadForm(NewThreadFormBase):
    def type_fields(self):
        if self.request.acl.threads.can_make_polls(self.forum):
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

    def clean_poll_question(self):
        data = self.cleaned_data['poll_question'].strip()
        if data:
            if len(data) < 3:
                raise forms.ValidationError(_("Poll quesiton should be at least three characters long."))
            if len(data) > 255:
                raise forms.ValidationError(_("Poll quesiton should be no longer than 250 characters."))
        return data

    def clean_poll_choices(self):
        self.clean_choices = []
        data = self.cleaned_data['poll_choices']

        if data:
            for choice in data.splitlines():
                choice = choice.strip()
                if not choice in self.clean_choices:
                    if len(choice) < 3:
                        raise forms.ValidationError(_("Poll choices should be at least three characters long."))
                    if len(choice) > 250:
                        raise forms.ValidationError(_("Poll choices should be no longer than 250 characters."))
                    self.clean_choices.append(choice)
            if len(self.clean_choices) < 2:
                raise forms.ValidationError(_("Poll needs at least two choices."))
            if len(self.clean_choices) > 10:
                raise forms.ValidationError(_("Poll cannot have more than 10 choices."))

        return '\r\n'.join(self.clean_choices)

    def clean_poll_max_choices(self):
        data = self.cleaned_data['poll_max_choices']
        if data < 1:
            raise forms.ValidationError(_("Voters must be allowed to make at least one choice."))
        if data > len(self.clean_choices):
            raise forms.ValidationError(_("Users cannot cast more votes than there are options."))
        return data

    def clean_poll_length(self):
        data = self.cleaned_data['poll_length']
        if data < 0:
            raise forms.ValidationError(_("Poll length cannot be negative."))
        if data > 300:
            raise forms.ValidationError(_("Poll length cannot be longer than 300 days."))
        return data

    def clean(self):
        data = super(NewThreadForm, self).clean()
        try:
            if bool(data['poll_question']) != bool(self.clean_choices):
                if bool(data['poll_question']):
                    raise forms.ValidationError(_("You have to define poll choices."))
                else:
                    raise forms.ValidationError(_("You have to define poll question."))
        except KeyError:
            pass
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
                           forms.TypedMultipleChoiceField(choices=choices, coerce=int,
                                                          widget=forms.CheckboxSelectMultiple))
        else:
            self.add_field('options',
                           forms.TypedChoiceField(choices=choices, coerce=int,
                                                  widget=forms.RadioSelect))
