from ..execute import execute_fetch_all, execute_fetch_one


def test_query_is_executed_and_all_results_are_returned(user, other_user):
    results = execute_fetch_all("SELECT id FROM misago_users_user;")
    assert len(results) == 2

    results_flat = [row[0] for row in results]
    assert user.id in results_flat
    assert other_user.id in results_flat


def test_query_is_executed_and_one_result_is_returned(admin, user, other_user):
    results = execute_fetch_one("SELECT COUNT(*) FROM misago_users_user;")
    assert results == (3,)
