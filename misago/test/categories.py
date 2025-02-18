import pytest

from ..acl.models import Role
from ..attachments.models import Attachment
from ..categories.models import Category, CategoryRole, RoleCategoryACL
from ..notifications.models import Notification, WatchedThread
from ..permissions.models import CategoryGroupPermission
from ..readtracker.models import ReadCategory, ReadThread
from ..threads.models import (
    Attachment as LegacyAttachment,
    AttachmentType,
    Poll,
    PollVote,
    Post,
    PostEdit,
    PostLike,
    Thread,
)
from ..threads.test import post_poll, post_thread, reply_thread
from ..users.models import User, Group

__all__ = ["CategoryRelationsFactory"]


class CategoryRelationsFactory:
    category: Category

    user: User
    other_user: User
    group: Group

    attachment: Attachment
    category_group_permission: CategoryGroupPermission
    legacy_attachment: LegacyAttachment
    notification: Notification
    poll: Poll
    poll_vote: PollVote
    post_edit: PostEdit
    post_like: PostLike
    read_category: ReadCategory
    read_thread: ReadThread
    role_category_acl: RoleCategoryACL
    thread: Thread
    thread_first_post: Post
    thread_reply: Post
    watched_thread: WatchedThread

    def __init__(
        self,
        *,
        category: Category,
        user: User,
        other_user: User,
        group: Group,
    ):
        self.category = category

        self.user = user
        self.other_user = other_user
        self.group = group

        self.create_relations()

    def create_relations(self):
        self.thread = self.create_thread()
        self.thread_first_post = self.thread.first_post
        self.thread_reply = self.create_thread_reply()

        self.attachment = self.create_attachment()
        self.category_group_permission = self.create_category_group_permission()
        self.legacy_attachment = self.create_legacy_attachment()
        self.notification = self.create_notification()
        self.poll = self.create_poll()
        self.poll_vote = self.create_poll_vote()
        self.post_edit = self.create_post_edit()
        self.post_like = self.create_post_like()
        self.read_category = self.create_read_category()
        self.read_thread = self.create_read_thread()
        self.role_category_acl = self.create_role_category_acl()
        self.watched_thread = self.create_watched_thread()

        self.category.set_last_thread(self.thread)
        self.category.save()

    def create_attachment(self):
        return Attachment.objects.create(
            category=self.category,
            thread=self.thread,
            post=self.thread_reply,
            uploader_name="Anonymous",
            uploader_slug="anonymous",
            name="filename.txt",
            slug="filename-txt",
        )

    def create_category_group_permission(self) -> CategoryGroupPermission:
        return CategoryGroupPermission.objects.create(
            category=self.category,
            group=self.group,
            permission="TEST",
        )

    def create_legacy_attachment(self) -> LegacyAttachment:
        return LegacyAttachment.objects.create(
            secret="secret",
            filetype=AttachmentType.objects.order_by("id").first(),
            post=self.thread_reply,
            uploader=self.user,
            uploader_name=self.user.username,
            uploader_slug=self.user.slug,
            filename="filename.txt",
        )

    def create_notification(self) -> Notification:
        return Notification.objects.create(
            user=self.user,
            verb="TEST",
            actor=self.other_user,
            actor_name=self.other_user.username,
            category=self.category,
            thread=self.thread,
            thread_title=self.thread.title,
            post=self.thread_reply,
        )

    def create_poll(self) -> Poll:
        return post_poll(self.thread, self.user)

    def create_poll_vote(self) -> PollVote:
        return self.poll.pollvote_set.order_by("id").first()

    def create_post_edit(self) -> PostEdit:
        return PostEdit.objects.create(
            category=self.category,
            thread=self.thread,
            post=self.thread_reply,
            editor=self.user,
            editor_name=self.user.username,
            editor_slug=self.user.slug,
            edited_from="",
            edited_to="",
        )

    def create_post_like(self) -> PostLike:
        return PostLike.objects.create(
            category=self.category,
            thread=self.thread,
            post=self.thread_first_post,
            liker=self.other_user,
            liker_name=self.other_user.username,
            liker_slug=self.other_user.slug,
        )

    def create_read_category(self) -> ReadCategory:
        return ReadCategory.objects.create(
            user=self.user,
            category=self.category,
        )

    def create_read_thread(self) -> ReadThread:
        return ReadThread.objects.create(
            user=self.user,
            category=self.category,
            thread=self.thread,
        )

    def create_role_category_acl(self) -> RoleCategoryACL:
        return RoleCategoryACL.objects.create(
            role=Role.objects.order_by("id").first(),
            category=self.category,
            category_role=CategoryRole.objects.order_by("id").first(),
        )

    def create_thread(self) -> Thread:
        return post_thread(self.category, poster=self.user)

    def create_thread_reply(self) -> Post:
        return reply_thread(self.thread, poster=self.other_user)

    def create_watched_thread(self) -> WatchedThread:
        return WatchedThread.objects.create(
            user=self.user,
            category=self.category,
            thread=self.thread,
        )

    def assert_relations_are_deleted(self):
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

        self.legacy_attachment.refresh_from_db()
        assert (
            self.legacy_attachment.post is None
        ), "LegacyAttachment should marked for deletion"

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

        with pytest.raises(PostLike.DoesNotExist):
            """Notification PostLike be deleted when category is deleted"""
            self.post_like.refresh_from_db()

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

        with pytest.raises(WatchedThread.DoesNotExist):
            """WatchedThread should be deleted when category is deleted"""
            self.watched_thread.refresh_from_db()

    def assert_relations_are_moved(self, new_category: Category):
        self.attachment.refresh_from_db()
        assert not self.attachment.is_deleted, "Attachment was NOT marked for deletion"
        assert (
            self.attachment.category_id == new_category.id
        ), "Attachment category relation was not updated"

        with pytest.raises(CategoryGroupPermission.DoesNotExist):
            """CategoryGroupPermission should be deleted when category is deleted"""
            self.category_group_permission.refresh_from_db()

        self.legacy_attachment.refresh_from_db()
        assert (
            self.legacy_attachment.post_id == self.thread_reply.id
        ), "LegacyAttachment post was updated"

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

        self.post_like.refresh_from_db()
        assert (
            self.post_like.category_id == new_category.id
        ), "PostLike category relation was not updated"

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

        self.watched_thread.refresh_from_db()
        assert (
            self.watched_thread.category_id == new_category.id
        ), "WatchedThread category relation was not updated"
