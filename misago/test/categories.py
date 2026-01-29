from dataclasses import dataclass

import pytest

from ..acl.models import Role
from ..attachments.models import Attachment
from ..categories.models import Category, CategoryRole, RoleCategoryACL
from ..edits.create import create_post_edit
from ..edits.models import PostEdit
from ..likes.models import Like
from ..notifications.models import Notification, WatchedThread
from ..permissions.models import CategoryGroupPermission
from ..polls.models import Poll, PollVote
from ..readtracker.models import ReadCategory, ReadThread
from ..threads.models import Post, Thread
from ..threadupdates.create import create_test_thread_update
from ..threadupdates.models import ThreadUpdate

__all__ = ["CategoryRelations", "category_relations_factory"]


@pytest.fixture
def category_relations_factory(
    thread_factory, thread_reply_factory, user, other_user, members_group
):
    def _category_relations_factory(category: Category) -> "CategoryRelations":
        thread = thread_factory(category)
        thread_reply = thread_reply_factory(thread)
        thread_update = create_test_thread_update(thread, other_user)

        attachment = Attachment.objects.create(
            category=category,
            thread=thread,
            post=thread_reply,
            uploader_name="Anonymous",
            uploader_slug="anonymous",
            name="filename.txt",
            slug="filename-txt",
        )

        category_group_permission = CategoryGroupPermission.objects.create(
            category=category,
            group=members_group,
            permission="TEST",
        )

        like = Like.objects.create(
            category=category,
            thread=thread,
            post=thread.first_post,
            user=other_user,
            user_name=other_user.username,
            user_slug=other_user.slug,
        )

        notification = Notification.objects.create(
            user=user,
            verb="TEST",
            actor=other_user,
            actor_name=other_user.username,
            category=category,
            thread=thread,
            thread_title=thread.title,
            post=thread_reply,
        )

        poll = Poll.objects.create(
            category=category,
            thread=thread,
            starter=user,
            starter_name=user.username,
            starter_slug=user.slug,
            question="...",
            choices=[],
        )

        poll_vote = PollVote.objects.create(
            category=category,
            thread=thread,
            poll=poll,
            choice_id="aaaa",
            voter=user,
            voter_name=user.username,
            voter_slug=user.slug,
        )

        post_edit = create_post_edit(post=thread.first_post, user=other_user)

        read_category = ReadCategory.objects.create(
            user=user,
            category=category,
        )

        read_thread = ReadThread.objects.create(
            user=user,
            category=category,
            thread=thread,
        )

        role_category_acl = RoleCategoryACL.objects.create(
            role=Role.objects.order_by("id").first(),
            category=category,
            category_role=CategoryRole.objects.order_by("id").first(),
        )

        watched_thread = WatchedThread.objects.create(
            user=user,
            category=category,
            thread=thread,
        )

        return CategoryRelations(
            attachment=attachment,
            category_group_permission=category_group_permission,
            like=like,
            notification=notification,
            poll=poll,
            poll_vote=poll_vote,
            post_edit=post_edit,
            read_category=read_category,
            read_thread=read_thread,
            role_category_acl=role_category_acl,
            thread=thread,
            thread_first_post=thread.first_post,
            thread_reply=thread_reply,
            thread_update=thread_update,
            watched_thread=watched_thread,
        )

    return _category_relations_factory


@dataclass(frozen=True)
class CategoryRelations:
    attachment: Attachment
    category_group_permission: CategoryGroupPermission
    like: Like
    notification: Notification
    poll: Poll
    poll_vote: PollVote
    post_edit: PostEdit
    read_category: ReadCategory
    read_thread: ReadThread
    role_category_acl: RoleCategoryACL
    thread: Thread
    thread_first_post: Post
    thread_reply: Post
    thread_update: ThreadUpdate
    watched_thread: WatchedThread

    def assert_relations_deleted(self):
        self.attachment.refresh_from_db()
        assert self.attachment.is_deleted, "Attachment should be marked for deletion"
        assert (
            not self.attachment.category
        ), "Attachment category relation should be removed"
        assert (
            not self.attachment.thread
        ), "Attachment thread relation should be removed"
        assert not self.attachment.post, "Attachment post relation should be removed"

        with pytest.raises(CategoryGroupPermission.DoesNotExist):
            """CategoryGroupPermission should be deleted when category is deleted"""
            self.category_group_permission.refresh_from_db()

        with pytest.raises(Like.DoesNotExist):
            """Like should be deleted when category is deleted"""
            self.like.refresh_from_db()

        with pytest.raises(Notification.DoesNotExist):
            """Notification should be deleted when category is deleted"""
            self.notification.refresh_from_db()

        with pytest.raises(Poll.DoesNotExist):
            """Poll should be deleted when category is deleted"""
            self.poll.refresh_from_db()

        with pytest.raises(PollVote.DoesNotExist):
            """PollVote should be deleted when category is deleted"""
            self.poll_vote.refresh_from_db()

        with pytest.raises(PostEdit.DoesNotExist):
            """PostEdit should be deleted when category is deleted"""
            self.post_edit.refresh_from_db()

        with pytest.raises(ReadCategory.DoesNotExist):
            """ReadCategory should be deleted when category is deleted"""
            self.read_category.refresh_from_db()

        with pytest.raises(ReadThread.DoesNotExist):
            """ReadThread should be deleted when category is deleted"""
            self.read_thread.refresh_from_db()

        with pytest.raises(RoleCategoryACL.DoesNotExist):
            """RoleCategoryACL should be deleted when category is deleted"""
            self.role_category_acl.refresh_from_db()

        with pytest.raises(Thread.DoesNotExist):
            """Thread should be deleted when category is deleted"""
            self.thread.refresh_from_db()

        with pytest.raises(Post.DoesNotExist):
            """Thread's first post should be deleted when category is deleted"""
            self.thread_first_post.refresh_from_db()

        with pytest.raises(Post.DoesNotExist):
            """Thread reply should be deleted when category is deleted"""
            self.thread_reply.refresh_from_db()

        with pytest.raises(ThreadUpdate.DoesNotExist):
            """Thread update should be deleted when category is deleted"""
            self.thread_update.refresh_from_db()

        with pytest.raises(WatchedThread.DoesNotExist):
            """WatchedThread should be deleted when category is deleted"""
            self.watched_thread.refresh_from_db()

    def assert_relations_moved(self, new_category: Category):
        self.attachment.refresh_from_db()
        assert not self.attachment.is_deleted, "Attachment was marked for deletion"
        assert (
            self.attachment.category_id == new_category.id
        ), "Attachment category relation was not updated"

        with pytest.raises(CategoryGroupPermission.DoesNotExist):
            """CategoryGroupPermission should be deleted when category is deleted"""
            self.category_group_permission.refresh_from_db()

        self.like.refresh_from_db()
        assert (
            self.like.category_id == new_category.id
        ), "Like category relation was not updated"

        self.notification.refresh_from_db()
        assert (
            self.notification.category_id == new_category.id
        ), "Notification category relation was not updated"

        self.poll.refresh_from_db()
        assert (
            self.poll.category_id == new_category.id
        ), "Poll category relation was not updated"

        self.poll_vote.refresh_from_db()
        assert (
            self.poll_vote.category_id == new_category.id
        ), "PollVote category relation was not updated"

        self.post_edit.refresh_from_db()
        assert (
            self.post_edit.category_id == new_category.id
        ), "PostEdit category relation was not updated"

        with pytest.raises(ReadCategory.DoesNotExist):
            """ReadCategory should be deleted when category is deleted"""
            self.read_category.refresh_from_db()

        self.read_thread.refresh_from_db()
        assert (
            self.read_thread.category_id == new_category.id
        ), "ReadThread category relation was not updated"

        with pytest.raises(RoleCategoryACL.DoesNotExist):
            """RoleCategoryACL should be deleted when category is deleted"""
            self.role_category_acl.refresh_from_db()

        self.thread.refresh_from_db()
        assert (
            self.thread.category_id == new_category.id
        ), "Thread category relation was not updated"

        self.thread_first_post.refresh_from_db()
        assert (
            self.thread_first_post.category_id == new_category.id
        ), "Thread's first post's category relation was not updated"

        self.thread_reply.refresh_from_db()
        assert (
            self.thread_reply.category_id == new_category.id
        ), "Thread reply's category relation was not updated"

        self.thread_update.refresh_from_db()
        assert (
            self.thread_update.category_id == new_category.id
        ), "ThreadUpdate category relation was not updated"

        self.watched_thread.refresh_from_db()
        assert (
            self.watched_thread.category_id == new_category.id
        ), "WatchedThread category relation was not updated"
