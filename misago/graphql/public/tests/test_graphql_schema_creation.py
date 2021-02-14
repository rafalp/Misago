def test_public_executable_schema_has_been_created():
    from ..schema import public_schema  # pylint: disable=import-outside-toplevel

    assert public_schema
