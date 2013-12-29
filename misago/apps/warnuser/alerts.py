def you_have_been_warned(giver, receiver, warning):
    alert = receiver.alert(ugettext_lazy("%(username)s has increased your warning level.").message)
    alert.profile('username', giver)
    alert.save_all()


def your_warn_has_been_canceled(canceler, receiver):
    pass