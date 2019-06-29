import pytest

from ...models import SocialAuthProvider


@pytest.fixture
def provider(db):
    return SocialAuthProvider.objects.create(
        provider="facebook", is_active=True, order=0
    )


@pytest.fixture
def other_provider(db):
    return SocialAuthProvider.objects.create(provider="github", is_active=True, order=1)


@pytest.fixture
def disabled_provider(db):
    return SocialAuthProvider.objects.create(
        provider="google", is_active=False, order=0
    )
