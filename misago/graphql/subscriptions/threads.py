from ariadne import SubscriptionType

from ...pubsub.threads import threads_updates


threads_subscription = SubscriptionType()


@threads_subscription.source("threads")
async def threads_source(*_):
    async for event in threads_updates():
        yield event


@threads_subscription.field("threads")
def threads_resolver(obj, *_):
    return obj
