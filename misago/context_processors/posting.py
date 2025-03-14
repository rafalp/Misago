from django.http import HttpRequest

from ..parser.pygments import PYGMENTS_CHOICES


def syntax_highlighting(request: HttpRequest) -> tuple[tuple[str, str], ...]:
    return {"syntax_highlighting": PYGMENTS_CHOICES}
