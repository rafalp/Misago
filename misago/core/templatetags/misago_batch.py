from django import template


register = template.Library()


@register.filter
def batch(items, size):
    batch_size = 0
    batch_items = []

    for item in items:
        batch_size += 1
        batch_items.append(item)

        if batch_size == size:
            yield batch_items
            batch_size = 0
            batch_items = []

    if batch_items:
        yield batch_items


@register.filter
def batchnonefilled(items, size):
    batch_size = 0
    batch_items = []

    for item in items:
        batch_size += 1
        batch_items.append(item)

        if batch_size == size:
            yield batch_items
            batch_size = 0
            batch_items = []

    if batch_size:
        batch_items.extend([None] * (size - batch_size))
        yield batch_items
