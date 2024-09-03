from ..path import full_path


def test_full_path_context_processor_returns_full_path(rf):
    request = rf.get("/full/path/?query=string")
    context = full_path(request)
    assert context == {
        "path": "/full/path/",
        "full_path": "/full/path/?query=string",
    }
