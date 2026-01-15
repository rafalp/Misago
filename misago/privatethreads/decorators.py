from django.utils.translation import pgettext_lazy

from ..auth.decorators import login_required


private_threads_login_required = login_required(
    pgettext_lazy(
        "private thread login required error",
        "Sign in to view private threads",
    )
)
