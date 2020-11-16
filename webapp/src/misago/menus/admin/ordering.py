from ..models import MenuItem


def get_next_free_order():
    last = MenuItem.objects.last()
    if last:
        return last.order + 1
    return 0
