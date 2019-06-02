from .cutoffdate import get_cutoff_date


def make_read_aware(request, posts):
    if not posts:
        return

    if not hasattr(posts, "__iter__"):
        posts = [posts]

    make_read(posts)

    if request.user.is_anonymous:
        return

    cutoff_date = get_cutoff_date(request.settings, request.user)
    unresolved_posts = {}

    for post in posts:
        if post.posted_on > cutoff_date:
            post.is_read = False
            post.is_new = True
            unresolved_posts[post.pk] = post

    if unresolved_posts:
        queryset = request.user.postread_set.filter(post__in=unresolved_posts)
        for post_id in queryset.values_list("post_id", flat=True):
            unresolved_posts[post_id].is_read = True
            unresolved_posts[post_id].is_new = False


def make_read(posts):
    for post in posts:
        post.is_read = True
        post.is_new = False


def save_read(user, post):
    user.postread_set.create(category=post.category, thread=post.thread, post=post)
