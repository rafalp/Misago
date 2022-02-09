import pytest

from ..loaders import posts_loader, threads_loader


@pytest.fixture
def loaders_context():
    context = {}
    threads_loader.setup_context(context)
    posts_loader.setup_context(context)
    return context
