import pytest

from ..youtube import parse_youtube_link


@pytest.mark.parametrize("timestamp", ("", "1", "1s", "21", "21s"))
@pytest.mark.parametrize(
    "link,result",
    (
        # hostnames
        ("youtube.com/watch?v=F2-32q4AE-k", {"video": "F2-32q4AE-k"}),
        ("www.youtube.com/watch?v=F2-32q4AE-k", {"video": "F2-32q4AE-k"}),
        ("m.youtube.com/watch?v=F2-32q4AE-k", {"video": "F2-32q4AE-k"}),
        ("www.m.youtube.com/watch?v=F2-32q4AE-k", {"video": "F2-32q4AE-k"}),
        ("youtube-nocookie.com/watch?v=F2-32q4AE-k", {"video": "F2-32q4AE-k"}),
        ("www.youtube-nocookie.com/watch?v=F2-32q4AE-k", {"video": "F2-32q4AE-k"}),
        # paths
        ("youtube.com/watch/F2-32q4AE-k", {"video": "F2-32q4AE-k"}),
        ("youtube.com/v/F2-32q4AE-k", {"video": "F2-32q4AE-k"}),
        ("youtube.com/embed/F2-32q4AE-k", {"video": "F2-32q4AE-k"}),
        ("youtube.com/e/F2-32q4AE-k", {"video": "F2-32q4AE-k"}),
        ("youtube.com/shorts/F2-32q4AE-k", {"video": "F2-32q4AE-k"}),
        ("youtube.com/live/F2-32q4AE-k", {"video": "F2-32q4AE-k"}),
        # youtu.be
        ("youtu.be/04KB8dZq-nw", {"video": "04KB8dZq-nw"}),
    ),
)
@pytest.mark.parametrize("scheme", ("https://", "http://", "://", ""))
def test_parse_youtube_link(scheme, link, result, timestamp):
    final_link = scheme + link

    if timestamp:
        result = {"video": result["video"], "start": timestamp}
        if "?" in final_link:
            final_link += "&t=" + timestamp
        else:
            final_link += "?t=" + timestamp

    assert parse_youtube_link(final_link) == result
