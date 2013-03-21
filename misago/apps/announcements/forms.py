from misago.apps.threadtype.posting.forms import (NewThreadForm as NewThreadBaseForm,
                                                  EditThreadForm as EditThreadBaseForm)

class NewThreadForm(NewThreadBaseForm):
    include_thread_weight = False


class EditThreadForm(EditThreadBaseForm):
    include_thread_weight = False
    