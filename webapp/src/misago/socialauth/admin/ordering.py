from ..models import SocialAuthProvider


def get_next_free_order():
    last = SocialAuthProvider.objects.filter(is_active=True).last()
    if last:
        return last.order + 1
    return 0
