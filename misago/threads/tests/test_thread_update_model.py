from ..models import Thread, ThreadUpdate


def test_thread_update_context_model_returns_none_if_its_not_set():
    thread_update = ThreadUpdate()
    assert thread_update.context_model is None


def test_thread_update_context_model_returns_none_if_app_label_is_invalid():
    thread_update = ThreadUpdate(context_type="invalid_app.InvalidModel")
    assert thread_update.context_model is None


def test_thread_update_context_model_returns_none_if_model_name_is_invalid():
    thread_update = ThreadUpdate(context_type="misago_threads.InvalidModel")
    assert thread_update.context_model is None


def test_thread_update_context_model_returns_model_type():
    thread_update = ThreadUpdate(context_type="misago_threads.Thread")
    assert thread_update.context_model == Thread
