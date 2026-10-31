from .models import Category


def update_usernames(user, **kwargs):
    Category.objects.filter(last_poster=user).update(
        last_poster_name=user.username, last_poster_slug=user.slug
    )