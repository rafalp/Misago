def test_anonymize_user_thread(user, user_thread):
    user.anonymize_data(anonymous_username="Deleted")

    user_thread.refresh_from_db()
    user_thread.starter_name == "Deleted"
    user_thread.starter_slug == "deleted"
    user_thread.last_poster_name == "Deleted"
    user_thread.last_poster_slug == "deleted"


def test_anonymize_user_post(user, user_thread):
    post = user_thread.first_post

    user.anonymize_data(anonymous_username="Deleted")

    post.refresh_from_db()
    post.poster_name == "Deleted"
