import re
from urllib.parse import parse_qs, urlparse

YOUTUBE_HOSTS = (
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "www.m.youtube.com",
    "youtube-nocookie.com",
    "www.youtube-nocookie.com",
    "youtu.be",
    "www.youtu.be",
)

YOUTU_BE_HOSTS = (
    "youtu.be",
    "www.youtu.be",
)

YOUTUBE_VIDEO_PATTERNS = (
    re.compile(r"^/watch/(?P<video>([0-9A-Za-z]|-|_)*)"),
    re.compile(r"^/v/(?P<video>([0-9A-Za-z]|-|_)*)"),
    re.compile(r"^/embed/(?P<video>([0-9A-Za-z]|-|_)*)"),
    re.compile(r"^/e/(?P<video>([0-9A-Za-z]|-|_)*)"),
    re.compile(r"^/shorts/(?P<video>([0-9A-Za-z]|-|_)*)"),
    re.compile(r"^/live/(?P<video>([0-9A-Za-z]|-|_)*)"),
)


def parse_youtube_link(link: str) -> dict | None:
    if not (
        link.lower().startswith("https://")
        or link.lower().startswith("http://")
        or link.startswith("://")
    ):
        link = "https://" + link

    if link.startswith("://"):
        link = "https" + link

    parsed_link = urlparse(link)

    if parsed_link.netloc.lower() not in YOUTUBE_HOSTS:
        return None

    query_dict = parse_qs(parsed_link.query) if parsed_link.query else {}
    timestamp = get_youtube_timestamp(query_dict)

    if parsed_link.netloc.lower() in YOUTU_BE_HOSTS:
        return _parse_youtu_be_link(parsed_link, timestamp)

    if result := _parse_youtube_path(parsed_link.path):
        if timestamp:
            result["start"] = timestamp
        return result

    if not query_dict.get("v"):
        return None

    for video in query_dict["v"]:
        if video := video.strip():
            result = {"video": video}
            if timestamp:
                result["start"] = timestamp
            return result

    return None


def _parse_youtu_be_link(parsed_link, timestamp: str) -> dict | None:
    if not parsed_link.path:
        return None

    if not parsed_link.path[0] == "/":
        return None

    video = parsed_link.path[1:]
    if "/" in video:
        video = video[: video.index("/")]

    if not video:
        return None

    result = {"video": video}

    if timestamp:
        result["start"] = timestamp

    return result


def _parse_youtube_path(path: str) -> dict | None:
    for video_pattern in YOUTUBE_VIDEO_PATTERNS:
        if match := video_pattern.match(path):
            return {"video": match.group("video")}

    return None


TIMESTAMP_RE = re.compile(r"^[1-9][0-9]*s?$")


def get_youtube_timestamp(query_dict: dict) -> str | None:
    if not query_dict.get("t"):
        return None

    for timestamp in query_dict["t"]:
        if TIMESTAMP_RE.match(timestamp):
            return timestamp

    return None
