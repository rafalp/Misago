from ..models import MenuLink


def get_next_free_order():
    last = MenuLink.objects.last()
    if last:
        return last.order + 1
    return 0
