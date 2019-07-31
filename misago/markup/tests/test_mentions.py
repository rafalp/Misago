from ..mentions import add_mentions


def test_util_replaces_mention_with_link_to_user_profile_in_parsed_text(
    request_mock, user
):
    parsing_result = {"parsed_text": f"<p>Hello, @{user.username}!</p>", "mentions": []}
    add_mentions(request_mock, parsing_result)
    assert parsing_result["parsed_text"] == (
        f'<p>Hello, <a href="{user.get_absolute_url()}">@{user.username}</a>!</p>'
    )


def test_util_adds_mention_to_parsig_result(request_mock, user):
    parsing_result = {"parsed_text": f"<p>Hello, @{user.username}!</p>", "mentions": []}
    add_mentions(request_mock, parsing_result)
    assert parsing_result["mentions"] == [user]


def test_mentions_arent_added_for_nonexisting_user(request_mock, user):
    parsing_result = {"parsed_text": f"<p>Hello, @OtherUser!</p>", "mentions": []}
    add_mentions(request_mock, parsing_result)
    assert parsing_result["parsed_text"] == "<p>Hello, @OtherUser!</p>"


def test_util_replaces_multiple_mentions_with_link_to_user_profiles_in_parsed_text(
    request_mock, user, other_user
):
    parsing_result = {
        "parsed_text": f"<p>Hello, @{user.username} and @{other_user.username}!</p>",
        "mentions": [],
    }
    add_mentions(request_mock, parsing_result)
    assert (
        f'<a href="{user.get_absolute_url()}">@{user.username}</a>'
        in parsing_result["parsed_text"]
    )
    assert (
        f'<a href="{other_user.get_absolute_url()}">@{other_user.username}</a>'
        in parsing_result["parsed_text"]
    )


def test_util_adds_multiple_mentions_to_parsig_result(request_mock, user, other_user):
    parsing_result = {
        "parsed_text": f"<p>Hello, @{user.username} and @{other_user.username}!</p>",
        "mentions": [],
    }
    add_mentions(request_mock, parsing_result)
    assert parsing_result["mentions"] == [user, other_user]


def test_util_handles_repeated_mentions_of_same_user(request_mock, user):
    parsing_result = {
        "parsed_text": f"<p>Hello, @{user.username} and @{user.username}!</p>",
        "mentions": [],
    }
    add_mentions(request_mock, parsing_result)
    assert parsing_result["mentions"] == [user]


def test_util_skips_mentions_in_links(request_mock, user, snapshot):
    parsing_result = {
        "parsed_text": f'<p>Hello, <a href="/">@{user.username}</a></p>',
        "mentions": [],
    }
    add_mentions(request_mock, parsing_result)
    assert parsing_result["parsed_text"] == (
        f'<p>Hello, <a href="/">@{user.username}</a></p>'
    )
    assert parsing_result["mentions"] == []


def test_util_handles_text_without_mentions(request_mock):
    parsing_result = {"parsed_text": f"<p>Hello, world!</p>", "mentions": []}
    add_mentions(request_mock, parsing_result)
    assert parsing_result["parsed_text"] == ("<p>Hello, world!</p>")
    assert parsing_result["mentions"] == []
