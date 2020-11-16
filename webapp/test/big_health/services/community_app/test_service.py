import pytest

from big_health.services.community_app.service import CommunityApp as CommunityAppService


class TestCommunityApp:

    @pytest.fixture
    def instance(self):
        return CommunityAppService()

    def test_loopback(self, instance: CommunityAppService):
        assert instance.loopback()
