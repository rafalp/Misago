from ..checksums import is_checksum_valid, make_checksum

message = "Test message."
post_pk = 123


def test_checksum_can_be_generated_for_post_message_and_pk():
    assert make_checksum(message, [post_pk])


def test_valid_message_checksum_is_checked():
    checksum = make_checksum(message, [post_pk])
    assert is_checksum_valid(message, checksum, [post_pk])


def test_checksum_invalidates_if_message_is_changed():
    checksum = make_checksum(message, [post_pk])
    assert not is_checksum_valid("Changed message.", checksum, [post_pk])


def test_checksum_invalidates_if_pk_is_changed():
    checksum = make_checksum(message, [post_pk])
    assert not is_checksum_valid(message, checksum, [post_pk + 1])
