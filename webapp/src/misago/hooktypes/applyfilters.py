from functools import partial, reduce


def apply_filters(action, hook, *args, **kwargs):
    if not hook:
        return action(*args, **kwargs)

    filtered_action = reduce(
        lambda chained_fns, next_fn: partial(next_fn, chained_fns), hook, action
    )
    return filtered_action(*args, **kwargs)
