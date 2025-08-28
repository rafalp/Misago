from ..members import private_thread_has_members


def test_private_thread_has_members_returns_true_if_thread_has_members(
    user_private_thread,
):
    assert private_thread_has_members(user_private_thread)


def test_private_thread_has_members_returns_false_if_thread_has_no_members(
    private_thread,
):
    assert not private_thread_has_members(private_thread)
