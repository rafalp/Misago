def test_admin_executable_schema_has_been_created():
    from ..schema import admin_schema  # pylint: disable=import-outside-toplevel

    assert admin_schema
