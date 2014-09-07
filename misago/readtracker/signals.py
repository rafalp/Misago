from misago.forums.signals import move_forum_content
from misago.threads.signals import move_thread


"""
Signal handlers
"""
@receiver(move_forum_content)
def delete_forum_tracker(sender, **kwargs):
    sender.forumread_set.all().delete()
    sender.threadread_set.all().delete()


@receiver(move_thread)
def delete_thread_tracker(sender, **kwargs):
    sender.threadread_set.all().delete()
