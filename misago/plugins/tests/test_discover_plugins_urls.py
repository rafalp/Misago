from ..urlpatterns import discover_plugins_urlpatterns


def test_discover_plugins_urlpatterns_discovers_apps_with_urls():
    urlpatterns = discover_plugins_urlpatterns(["misago.threads", "misago.users"])
    assert len(urlpatterns) == 2


def test_discover_plugins_urlpatterns_skips_apps_without_urls():
    urlpatterns = discover_plugins_urlpatterns(["misago.core"])
    assert not urlpatterns
