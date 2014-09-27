def announce_thread(user, thread):
    if thread.weight < 2:
        thread.weight = 2
        thread.save(update_fields=['weight'])
        return True
    else:
        return False


def pin_thread(user, thread):
    if thread.weight < 1:
        thread.weight = 1
        thread.save(update_fields=['weight'])
        return True
    else:
        return False


def default_thread(user, thread):
    if thread.weight > 0:
        thread.weight = 0
        thread.save(update_fields=['weight'])
        return True
    else:
        return False


def move_thread(user, thread, new_forum):
    if thread.forum_id != new_forum.pk:
        thread.move(new_forum)
        thread.save(update_fields=['forum'])
        return True
    else:
        return False


def merge_thread(user, thread, other_thread):
    thread.merge(other_thread)
    thread.synchornize()
    thread.save()
    other_thread.delete()
    return True


def approve_thread(user, thread):
    if thread.is_moderated:
        thread.is_closed = False
        thread.first_post.is_moderated = False
        thread.first_post.save(update_fields=['is_moderated'])
        thread.synchornize()
        thread.save()
        return True
    else:
        return False


def open_thread(user, thread):
    if thread.is_closed:
        thread.is_closed = False
        thread.save(update_fields=['is_closed'])
        return True
    else:
        return False


def close_thread(user, thread):
    if not thread.is_closed:
        thread.is_closed = True
        thread.save(update_fields=['is_closed'])
        return True
    else:
        return False


def show_thread(user, thread):
    if thread.is_hidden:
        thread.first_post.is_hidden = False
        thread.first_post.save(update_fields=['is_hidden'])
        thread.is_hidden = False
        thread.save(update_fields=['is_hidden'])
        thread.synchornize()
        thread.save()
        return True
    else:
        return False


def hide_thread(user, thread):
    if not thread.is_hidden:
        thread.is_hidden = True
        thread.save(update_fields=['is_hidden'])
        return True
    else:
        return False


def delete_thread(user, thread):
    thread.delete()
    return True
