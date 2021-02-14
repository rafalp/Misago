from ..generic import parse_generic_scalar_literal, serialize_generic_scalar


TEST_SCALAR = {"test": True}


def test_parsing_literal_is_pass_through_op():
    parsed_value = parse_generic_scalar_literal(TEST_SCALAR)
    assert parsed_value == TEST_SCALAR


def test_serializing_generic_scalar_is_pass_through_op():
    serialized_value = serialize_generic_scalar(TEST_SCALAR)
    assert serialized_value == TEST_SCALAR
