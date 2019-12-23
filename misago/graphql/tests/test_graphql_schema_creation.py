def test_executable_schema_has_been_created():
    from ..schema import schema  # pylint: disable=import-outside-toplevel

    assert schema
