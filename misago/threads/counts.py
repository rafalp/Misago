def sync_user_unread_private_threads_count(user):
    if not user.sync_unread_private_threads:
        return

    # TODO: USE UTILS FROM PRIV THREADS TO COUNT STUFF
    user.unread_private_threads = 0
    user.sync_unread_private_threads = False

    user.save(update_fields=[
        'unread_private_threads',
        'sync_unread_private_threads'
    ])