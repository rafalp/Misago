import pytest

from ..acl.models import Role
from ..attachments.models import Attachment
from ..categories.models import Category, CategoryRole, RoleCategoryACL
from ..notifications.models import Notification, WatchedThread
from ..permissions.models import CategoryGroupPermission
from ..readtracker.models import ReadCategory, ReadThread
from ..threads.models import Post, Thread
from ..threads.test import post_poll, post_thread, reply_thread
from ..users.models import User, Group


class CategoryRelationsFactory:
    category: Category

    user: User
    other_user: User
    group: Group

    attachment: Attachment
    category_group_permission: CategoryGroupPermission
    notification: Notification
    read_category: ReadCategory
    read_thread: ReadThread
    role_category_acl: RoleCategoryACL
    thread: Thread
    thread_first_post: Post
    thread_reply: Post
    watched_thread: WatchedThread

    def __init__(
        self,
        category: Category,
        *,
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
        self.notification = self.create_notification()
        self.read_category = self.create_read_category()
        self.read_thread = self.create_read_thread()
        self.role_category_acl = self.create_role_category_acl()
        self.watched_thread = self.crea()

    def create_attachment(self):
        return Attachment.objects.create(
            category=self.category,
            thread=self.thread,
            post=self.thread_reply,
            uploader_name="Anonymous",
            uploader_slug="anonymous",
            secret="secret",
            name="filename.txt",
            slug="filename-txt",
        )

    def create_category_group_permission(self) -> CategoryGroupPermission:
        return CategoryGroupPermission.objects.create(
            category=self.category,
            group=self.group,
            permission="TEST",
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
        assert self.attachment.is_deleted, "Attachment was marked for deletion"
        assert not self.attachment.category, "Attachment category relation was removed"
        assert not self.attachment.thread, "Attachment thread relation was removed"
        assert not self.attachment.post, "Attachment post relation was removed"

        with pytest.raises(CategoryGroupPermission.DoesNotExist):
            """CategoryGroupPermission should be deleted when category is deleted"""
            self.category_group_permission.refresh_from_db()

        with pytest.raises(Notification.DoesNotExist):
            """Notification should be deleted when category is deleted"""
            self.notification.refresh_from_db()

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
        ), "Attachment category relation was updated"

        with pytest.raises(CategoryGroupPermission.DoesNotExist):
            """CategoryGroupPermission should be deleted when category is deleted"""
            self.category_group_permission.refresh_from_db()

        self.notification.refresh_from_db()
        assert (
            self.notification.category_id == new_category.id
        ), "Notification category relation was updated"

        with pytest.raises(ReadCategory.DoesNotExist):
            """ReadCategory should be deleted when category is deleted"""
            self.read_category.refresh_from_db()

        self.read_thread.refresh_from_db()
        assert (
            self.read_thread.category_id == new_category.id
        ), "ReadThread category relation was updated"

        with pytest.raises(RoleCategoryACL.DoesNotExist):
            """RoleCategoryACL should be deleted when category is deleted"""
            self.role_category_acl.refresh_from_db()

        self.thread.refresh_from_db()
        assert (
            self.thread.category_id == new_category.id
        ), "Thread category relation was updated"

        self.thread_first_post.refresh_from_db()
        assert (
            self.thread_first_post.category_id == new_category.id
        ), "Thread's first post's category relation was updated"

        self.thread_reply.refresh_from_db()
        assert (
            self.thread_reply.category_id == new_category.id
        ), "Thread reply's category relation was updated"

        self.watched_thread.refresh_from_db()
        assert (
            self.watched_thread.category_id == new_category.id
        ), "WatchedThread category relation was updated"
