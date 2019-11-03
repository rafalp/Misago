from ..utils import generate_version_string


def test_util_generates_version_string():
    assert generate_version_string()
