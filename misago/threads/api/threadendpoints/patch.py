from misago.core.apipatchrouter import ApiPatchRouter
from misago.threads.moderation import threads as moderation

thread_patch_endpoint = ApiPatchRouter()


def patch_weight(request, thread, value):
    if value == 2:
        moderation.pin_thread_globally(request.user, thread)
    if value == 1:
        moderation.pin_thread_locally(request.user, thread)
    if value == 0:
        moderation.unpin_thread(request.user, thread)

    return {'weight': thread.weight}
thread_patch_endpoint.replace('weight', patch_weight)


def patch_subscribtion(request, thread, value):
    request.user.subscription_set.filter(thread=thread).delete()

    if value == 'notify':
        thread.subscription = request.user.subscription_set.create(
            thread=thread,
            category=thread.category,
            last_read_on=thread.last_post_on,
            send_email=False,
        )

        return {'subscription': False}
    elif value == 'email':
        thread.subscription = request.user.subscription_set.create(
            thread=thread,
            category=thread.category,
            last_read_on=thread.last_post_on,
            send_email=True,
        )

        return {'subscription': True}
    else:
        return {'subscription': None}
thread_patch_endpoint.replace('subscription', patch_subscribtion)