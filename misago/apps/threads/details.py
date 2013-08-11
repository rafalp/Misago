from misago.apps.threadtype.details import DetailsBaseView, KarmaVotesBaseView
from misago.apps.threads.mixins import TypeMixin

class DetailsView(DetailsBaseView, TypeMixin):
    pass


class KarmaVotesView(KarmaVotesBaseView, TypeMixin):
    pass