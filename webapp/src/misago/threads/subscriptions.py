from .models import Subscription


def make_subscription_aware(user, target):
    if hasattr(target, "__iter__"):
        make_threads_subscription_aware(user, target)
    else:
        make_thread_subscription_aware(user, target)


def make_threads_subscription_aware(user, threads):
    if not threads:
        return

    if user.is_anonymous:
        for thread in threads:
            thread.subscription = None
    else:
        threads_dict = {}
        for thread in threads:
            thread.subscription = None
            threads_dict[thread.pk] = thread

        subscriptions_queryset = user.subscription_set.filter(
            thread_id__in=threads_dict.keys()
        )

        for subscription in subscriptions_queryset.iterator():
            threads_dict[subscription.thread_id].subscription = subscription


def make_thread_subscription_aware(user, thread):
    if user.is_anonymous:
        thread.subscription = None
    else:
        try:
            thread.subscription = user.subscription_set.get(thread=thread)
        except Subscription.DoesNotExist:
            thread.subscription = None
