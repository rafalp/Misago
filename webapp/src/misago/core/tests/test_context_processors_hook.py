from ..context_processors import hooks


def test_context_processors_hook_can_inject_context(mocker):
    plugin = mocker.Mock(return_value={"plugin": True})
    mocker.patch("misago.core.context_processors.context_processors_hooks", [plugin])
    context = hooks(None)
    assert context == {"plugin": True}
