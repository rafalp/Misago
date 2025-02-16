from ..parser import parse


def test_parser_converts_unmarked_links_to_hrefs(request_mock, user, snapshot):
    text = "Lorem ipsum http://test.com"
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]


def test_parser_skips_links_in_inline_code_markdown(request_mock, user, snapshot):
    text = "Lorem ipsum `http://test.com`"
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]


def test_parser_skips_links_in_inline_code_bbcode(request_mock, user, snapshot):
    text = "Lorem ipsum [code]http://test.com[/code]"
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]


def test_parser_skips_links_in_code_bbcode(request_mock, user, snapshot):
    text = """
[code]
http://test.com
[/code]
    """
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]


def test_absolute_link_to_site_is_changed_to_relative_link(
    request_mock, user, snapshot
):
    text = "clean_links step cleans http://example.com"
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]


def test_absolute_link_to_site_is_added_to_internal_links_list(request_mock, user):
    text = "clean_links step cleans http://example.com"
    result = parse(text, request_mock, user)
    assert result["internal_links"] == ["/"]


def test_absolute_link_to_site_without_schema_is_changed_to_relative_link(
    request_mock, user, snapshot
):
    text = "clean_links step cleans example.com"
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]


def test_absolute_link_to_site_without_schema_is_added_to_internal_links_list(
    request_mock, user
):
    text = "clean_links step cleans example.com"
    result = parse(text, request_mock, user)
    assert result["internal_links"] == ["/"]


def test_absolute_link_with_path_to_site_is_changed_to_relative_link(
    request_mock, user, snapshot
):
    text = "clean_links step cleans http://example.com/somewhere-something/"
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]


def test_absolute_link_with_path_to_site_is_added_to_internal_links_list(
    request_mock, user
):
    text = "clean_links step cleans http://example.com/somewhere-something/"
    result = parse(text, request_mock, user)
    assert result["internal_links"] == ["/somewhere-something/"]


def test_full_link_with_path_text_is_set_to_domain_and_path(request_mock, user):
    text = "clean_links step cleans http://example.com/somewhere-something/"
    result = parse(text, request_mock, user)
    assert ">example.com/somewhere-something/<" in result["parsed_text"]


def test_outgoing_link_is_added_to_outgoing_links_list(request_mock, user):
    text = "clean_links step cleans https://other.com"
    result = parse(text, request_mock, user)
    assert result["outgoing_links"] == ["other.com"]


def test_outgoing_llink_includes_external_nofollow_and_noopener(request_mock, user):
    text = "Lorem [url]https://dummyimage.com/g/1200/500[/url] ipsum"
    result = parse(text, request_mock, user)
    assert 'rel="external nofollow noopener"' in result["parsed_text"]


def test_outgoing_link_without_scheme_is_added_to_outgoing_links_list(
    request_mock, user
):
    text = "clean_links step cleans other.com"
    result = parse(text, request_mock, user)
    assert result["outgoing_links"] == ["other.com"]


def test_outgoing_link_with_path_is_added_to_outgoing_links_list(request_mock, user):
    text = "clean_links step cleans other.com/some/path/"
    result = parse(text, request_mock, user)
    assert result["outgoing_links"] == ["other.com/some/path/"]


def test_local_image_is_changed_to_relative_link(request_mock, user, snapshot):
    text = "clean_links step cleans !(example.com/media/img.png)"
    result = parse(text, request_mock, user)
    assert snapshot == result["parsed_text"]


def test_local_image_is_added_to_images_list(request_mock, user):
    text = "clean_links step cleans !(example.com/media/img.png)"
    result = parse(text, request_mock, user)
    assert result["images"] == ["/media/img.png"]


def test_remote_image_is_added_to_images_list(request_mock, user):
    text = "clean_links step cleans !(other.com/media/img.png)"
    result = parse(text, request_mock, user)
    assert result["images"] == ["other.com/media/img.png"]


def test_local_image_link_is_added_to_images_and_links_lists(request_mock, user):
    text = "clean_links step cleans [!(example.com/media/img.png)](example.com/test/)"
    result = parse(text, request_mock, user)
    assert result["internal_links"] == ["/test/"]
    assert result["images"] == ["/media/img.png"]


def test_remote_image_link_is_added_to_images_and_links_lists(request_mock, user):
    text = "clean_links step cleans [!(other.com/media/img.png)](other.com/test/)"
    result = parse(text, request_mock, user)
    assert result["outgoing_links"] == ["other.com/test/"]
    assert result["images"] == ["other.com/media/img.png"]


def test_parser_skips_shva_in_attachment_link_querystring_if_force_option_is_omitted(
    request_mock, user
):
    text = "clean_links step cleans ![3.png](http://example.com/a/thumb/test/43/)"
    result = parse(text, request_mock, user)
    assert "?shva=1" not in result["parsed_text"]
