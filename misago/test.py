def assert_contains(response, string, status_code=200):
    assert response.status_code == status_code
    fail_message = f'"{string}" not found in response.content'
    assert string in response.content.decode("utf-8"), fail_message


def assert_not_contains(response, string, status_code=200):
    assert response.status_code == status_code
    fail_message = f'"{string}" was found in response.content'
    assert string not in response.content.decode("utf-8"), fail_message
