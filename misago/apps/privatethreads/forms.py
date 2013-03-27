from django import forms
from misago.forms import Form
from misago.apps.threadtype.posting.forms import (NewThreadForm as NewThreadBaseForm,
                                                  EditThreadForm as EditThreadBaseForm,
                                                  NewReplyForm as NewReplyBaseForm,
                                                  EditReplyForm as EditReplyBaseForm)

class NewThreadForm(NewThreadBaseForm):
    include_thread_weight = False
    include_close_thread = False


class EditThreadForm(EditThreadBaseForm):
    include_thread_weight = False
    include_close_thread = False


class NewReplyForm(NewReplyBaseForm):
    include_thread_weight = False
    include_close_thread = False


class EditReplyForm(EditReplyBaseForm):
    include_thread_weight = False
    include_close_thread = False


class InviteMemberForm(Form):
    username = forms.CharField(max_length=200)