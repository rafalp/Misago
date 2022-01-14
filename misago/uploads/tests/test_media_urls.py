from ..urls import make_media_url


def test_media_path_is_converted_to_url():
    url = make_media_url("avatars/test.png")
    assert url == "/media/avatars/test.png"
