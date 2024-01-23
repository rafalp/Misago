from django.conf import settings

from ..conf.dynamicsettings import DynamicSettings


class ForumAddress:
    current_address: str | None
    hostnames: list[str]

    def __init__(self, settings_: DynamicSettings | None):
        self.current_address = settings_.forum_address or None
        self.hostnames = []

        if settings_.forum_address:
            self.hostnames.append(self.get_hostname(settings_.forum_address))

        for historic_address in settings.MISAGO_FORUM_ADDRESS_HISTORY:
            self.hostnames.append(self.get_hostname(historic_address))

    def is_inbound_link(self, link: str) -> bool:
        return self.get_hostname(link) in self.hostnames

    def get_hostname(self, link: str) -> str:
        if "://" in link:
            link = link[link.index("://") + 3 :]
        if "/" in link:
            link = link[: link.index("/")]

        return link.lower()
