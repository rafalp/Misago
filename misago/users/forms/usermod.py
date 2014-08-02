from misago.users.forms.admin import BanUsersForm


class BanForm(BanUsersForm):
    def __init__(self *args, **kwargs):
        self.user = kwargs.pop('user')
        super(BanForm, self).__init__(*args, **kwargs)
