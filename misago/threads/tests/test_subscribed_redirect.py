def test_threads_subscribed_list_redirects_to_watched(db, client):
    response = client.get("/subscribed/")
    assert response.status_code == 301
    assert response.headers["location"] == "/watched/"


def test_category_subscribed_list_redirects_to_watched(db, client, default_category):
    response = client.get(default_category.get_absolute_url() + "subscribed/")
    assert response.status_code == 301
    assert (
        response.headers["location"] == default_category.get_absolute_url() + "watched/"
    )


def test_private_threads_subscribed_list_redirects_to_watched(db, client):
    response = client.get("/private-threads/subscribed/")
    assert response.status_code == 301
    assert response.headers["location"] == "/private-threads/watched/"
