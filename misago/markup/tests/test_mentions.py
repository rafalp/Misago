from ..htmlparser import parse_html_string, print_html_string
from ..mentions import add_mentions


def test_util_replaces_mention_with_link_to_user_profile_in_parsed_text(user):
    parsing_result = {"parsed_text": f"<p>Hello, @{user.username}!</p>", "mentions": []}
    root_node = parse_html_string(parsing_result["parsed_text"])

    add_mentions(parsing_result, root_node)

    parsing_result["parsed_text"] = print_html_string(root_node)
    assert parsing_result["parsed_text"] == (
        f'<p>Hello, <a href="{user.get_absolute_url()}" '
        f'data-quote="@{user.username}">@{user.username}</a>!</p>'
    )


def test_util_adds_mention_to_parsig_result(user):
    parsing_result = {"parsed_text": f"<p>Hello, @{user.username}!</p>", "mentions": []}
    root_node = parse_html_string(parsing_result["parsed_text"])

    add_mentions(parsing_result, root_node)

    parsing_result["parsed_text"] = print_html_string(root_node)
    assert parsing_result["mentions"] == [user.id]


def test_mentions_arent_added_for_nonexisting_user(user):
    parsing_result = {"parsed_text": f"<p>Hello, @OtherUser!</p>", "mentions": []}
    root_node = parse_html_string(parsing_result["parsed_text"])

    add_mentions(parsing_result, root_node)

    parsing_result["parsed_text"] = print_html_string(root_node)
    assert parsing_result["parsed_text"] == "<p>Hello, @OtherUser!</p>"


def test_util_replaces_multiple_mentions_with_link_to_user_profiles_in_parsed_text(
    user, other_user
):
    parsing_result = {
        "parsed_text": f"<p>Hello, @{user.username} and @{other_user.username}!</p>",
        "mentions": [],
    }
    root_node = parse_html_string(parsing_result["parsed_text"])

    add_mentions(parsing_result, root_node)

    parsing_result["parsed_text"] = print_html_string(root_node)
    assert (
        f'<a href="{user.get_absolute_url()}" '
        f'data-quote="@{user.username}">@{user.username}</a>'
    ) in parsing_result["parsed_text"]
    assert (
        f'<a href="{other_user.get_absolute_url()}" '
        f'data-quote="@{other_user.username}">@{other_user.username}</a>'
    ) in parsing_result["parsed_text"]


def test_util_adds_multiple_mentions_to_parsig_result(user, other_user):
    parsing_result = {
        "parsed_text": f"<p>Hello, @{user.username} and @{other_user.username}!</p>",
        "mentions": [],
    }
    root_node = parse_html_string(parsing_result["parsed_text"])

    add_mentions(parsing_result, root_node)

    parsing_result["parsed_text"] = print_html_string(root_node)
    assert parsing_result["mentions"] == [user.id, other_user.id]


def test_util_handles_repeated_mentions_of_same_user(user):
    parsing_result = {
        "parsed_text": f"<p>Hello, @{user.username} and @{user.username}!</p>",
        "mentions": [],
    }
    root_node = parse_html_string(parsing_result["parsed_text"])

    add_mentions(parsing_result, root_node)

    parsing_result["parsed_text"] = print_html_string(root_node)
    assert parsing_result["mentions"] == [user.id]


def test_util_skips_mentions_in_links(user, snapshot):
    parsing_result = {
        "parsed_text": f'<p>Hello, <a href="/">@{user.username}</a></p>',
        "mentions": [],
    }
    root_node = parse_html_string(parsing_result["parsed_text"])

    add_mentions(parsing_result, root_node)

    parsing_result["parsed_text"] = print_html_string(root_node)
    assert parsing_result["parsed_text"] == (
        f'<p>Hello, <a href="/">@{user.username}</a></p>'
    )
    assert parsing_result["mentions"] == []


def test_util_handles_text_without_mentions(db):
    parsing_result = {"parsed_text": f"<p>Hello, world!</p>", "mentions": []}
    root_node = parse_html_string(parsing_result["parsed_text"])

    add_mentions(parsing_result, root_node)

    parsing_result["parsed_text"] = print_html_string(root_node)
    assert parsing_result["parsed_text"] == ("<p>Hello, world!</p>")
    assert parsing_result["mentions"] == []
