from ..path import path


def test_path_context_processor_returns_paths(rf):
    request = rf.get("/full/path/?query=string")
    context = path(request)
    assert context == {
        "path": "/full/path/",
        "full_path": "/full/path/?query=string",
    }
