from django.utils.translation import pgettext_lazy

from ..auth.decorators import login_required

private_threads_search_login_required = login_required(
    pgettext_lazy(
        "private threads search login required error",
        "Sign in to search private threads",
    )
)
