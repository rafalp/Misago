from broadcaster import Broadcast

from ..conf import settings

broadcast = Broadcast(settings.pubsub_url)
