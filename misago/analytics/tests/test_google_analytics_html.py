from ...conf.test import override_dynamic_settings
from ...test import assert_contains, assert_not_contains


@override_dynamic_settings(google_tracking_id=None)
def test_tracking_script_is_not_included_if_tracking_id_is_not_set(db, client):
    response = client.get("/")
    assert_not_contains(response, "googletagmanager.com/gtag/js")


@override_dynamic_settings(google_tracking_id="UA-TEST")
def test_tracking_script_is_included_if_tracking_id_is_not_set(db, client):
    response = client.get("/")
    assert_contains(response, "googletagmanager.com/gtag/js")
    assert_contains(response, "UA-TEST")
