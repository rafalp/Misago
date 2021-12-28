from httpx import Response


def assert_contains(
    response: Response,
    value: str,
    msg: str = None,
    *,
    status_code: int = 200,
    not_contains: bool = False,
):
    assert isinstance(
        response, Response
    ), f"expected response of type Response, received {type(response)}"
    assert response.status_code == status_code, (
        f"expected response with status code {status_code}, "
        f"received {response.status_code}"
    )
    assert response.headers["content-type"] == "text/html; charset=utf-8", (
        "expected response with content type 'text/html; charset=utf-8', "
        f"received {response.headers['content-type']}"
    )

    bytes_string = value.encode("utf-8")
    if not_contains:
        assert bytes_string not in response.content, msg or (
            f"Expected response to don't contain '{value}'"
        )
    else:
        assert bytes_string in response.content, msg or (
            f"Expected response to contain '{value}'"
        )


def assert_not_contains(
    response: Response, value: str, msg: str = None, *, status_code: int = 200
):
    return assert_contains(
        response, value, msg, status_code=status_code, not_contains=True
    )
