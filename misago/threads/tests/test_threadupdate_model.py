from ..models import Thread, ThreadUpdate


def test_threadupdate_context_model_returns_none_if_its_not_set():
    threadupdate = ThreadUpdate()
    assert threadupdate.context_model is None


def test_threadupdate_context_model_returns_none_if_app_label_is_invalid():
    threadupdate = ThreadUpdate(context_type="invalid_app.InvalidModel")
    assert threadupdate.context_model is None


def test_threadupdate_context_model_returns_none_if_model_name_is_invalid():
    threadupdate = ThreadUpdate(context_type="misago_threads.InvalidModel")
    assert threadupdate.context_model is None


def test_threadupdate_context_model_returns_model_type():
    threadupdate = ThreadUpdate(context_type="misago_threads.Thread")
    assert threadupdate.context_model == Thread
