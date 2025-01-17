from collections import namedtuple

import pytest

from ...acl.models import Role
from ...attachments.models import Attachment
from ...notifications.models import Notification, WatchedThread
from ...permissions.models import CategoryGroupPermission
from ...readtracker.models import ReadCategory, ReadThread
from ...threads.models import (
    Attachment as LegacyAttachment,
    AttachmentType,
    Poll,
    PollVote,
    Post,
    PostEdit,
    PostLike,
    Subscription,
    Thread,
)
from ...threads.test import post_thread, post_poll
from ..delete import delete_category
from ..models import Category, CategoryRole, RoleCategoryACL
from ..mptt import heal_category_trees


def test_delete_category_raises_value_error_if_contents_will_be_moved_to_deleted_category(
    default_category,
):
    with pytest.raises(ValueError) as exc_info:
        delete_category(default_category, move_contents_to=default_category)

    assert str(exc_info.value) == "Category from 'move_contents_to' will be deleted."


def test_delete_category_raises_value_error_if_contents_will_be_moved_to_deleted_child_category(
    default_category,
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    default_category.refresh_from_db()

    with pytest.raises(ValueError) as exc_info:
        delete_category(
            default_category,
            move_children_to=None,
            move_contents_to=child_category,
        )

    assert str(exc_info.value) == "Category from 'move_contents_to' will be deleted."


def test_delete_category_raises_value_error_if_child_categories_will_be_moved_to_deleted_category(
    default_category,
):
    with pytest.raises(ValueError) as exc_info:
        delete_category(default_category, move_children_to=default_category)

    assert str(exc_info.value) == "Category from 'move_children_to' will be deleted."


def test_delete_category_raises_value_error_if_child_categories_will_be_moved_to_deleted_child_category(
    default_category,
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    default_category.refresh_from_db()

    with pytest.raises(ValueError) as exc_info:
        delete_category(default_category, move_children_to=child_category)

    assert str(exc_info.value) == "Category from 'move_children_to' will be deleted."


def test_delete_category_deletes_category(default_category):
    delete_category(default_category)

    with pytest.raises(Category.DoesNotExist):
        default_category.refresh_from_db()


CategoryContents = namedtuple(
    "CategoryContents",
    (
        "attachment",
        "category_group_permission",
        "category_role",
        "legacy_attachment",
        "notification",
        "poll",
        "poll_vote",
        "post",
        "post_edit",
        "post_like",
        "read_category",
        "read_thread",
        "subscription",
        "thread",
        "watched_thread",
    ),
)


def create_category_contents(
    user, other_user, members_group, category
) -> CategoryContents:
    category_group_permission = CategoryGroupPermission.objects.create(
        category=category,
        group=members_group,
        permission="TEST",
    )

    category_role = RoleCategoryACL.objects.create(
        role=Role.objects.order_by("id").first(),
        category=category,
        category_role=CategoryRole.objects.order_by("id").first(),
    )

    thread = post_thread(category)
    post = thread.first_post

    post_edit = PostEdit.objects.create(
        category=category,
        thread=thread,
        post=post,
        editor=user,
        editor_name=user.username,
        editor_slug=user.slug,
        edited_from="",
        edited_to="",
    )

    post_like = PostLike.objects.create(
        category=category,
        thread=thread,
        post=post,
        liker=other_user,
        liker_name=other_user.username,
        liker_slug=other_user.slug,
    )

    attachment = Attachment.objects.create(
        category=category,
        thread=thread,
        post=post,
        uploader=user,
        uploader_name=user.username,
        uploader_slug=user.slug,
        secret="secret",
        name="filename.txt",
        slug="filename-txt",
    )

    legacy_attachment = LegacyAttachment.objects.create(
        secret="secret",
        filetype=AttachmentType.objects.order_by("id").first(),
        post=post,
        uploader=user,
        uploader_name=user.username,
        uploader_slug=user.slug,
        filename="filename.txt",
    )

    poll = post_poll(thread, user)
    poll_vote = poll.pollvote_set.order_by("id").first()

    subscription = Subscription.objects.create(
        user=user,
        thread=thread,
        category=category,
    )

    notification = Notification.objects.create(
        user=user,
        verb="TEST",
        actor=other_user,
        actor_name=other_user.username,
        category=category,
        thread=thread,
        thread_title=thread.title,
        post=post,
    )

    watched_thread = WatchedThread.objects.create(
        user=user,
        category=category,
        thread=thread,
    )

    read_category = ReadCategory.objects.create(
        user=user,
        category=category,
    )
    read_thread = ReadThread.objects.create(
        user=user,
        category=category,
        thread=thread,
    )

    return CategoryContents(
        attachment=attachment,
        category_group_permission=category_group_permission,
        category_role=category_role,
        legacy_attachment=legacy_attachment,
        notification=notification,
        poll=poll,
        poll_vote=poll_vote,
        post=post,
        post_edit=post_edit,
        post_like=post_like,
        read_category=read_category,
        read_thread=read_thread,
        subscription=subscription,
        thread=thread,
        watched_thread=watched_thread,
    )


def assert_category_contents_deleted(contents: CategoryContents):
    contents.attachment.refresh_from_db()
    assert contents.attachment.is_deleted

    with pytest.raises(CategoryGroupPermission.DoesNotExist):
        contents.category_group_permission.refresh_from_db()

    contents.legacy_attachment.refresh_from_db()
    assert contents.legacy_attachment.post is None

    with pytest.raises(Notification.DoesNotExist):
        contents.notification.refresh_from_db()

    with pytest.raises(Poll.DoesNotExist):
        contents.poll.refresh_from_db()

    with pytest.raises(PollVote.DoesNotExist):
        contents.poll_vote.refresh_from_db()

    with pytest.raises(Post.DoesNotExist):
        contents.post.refresh_from_db()

    with pytest.raises(PostEdit.DoesNotExist):
        contents.post_edit.refresh_from_db()

    with pytest.raises(PostLike.DoesNotExist):
        contents.post_like.refresh_from_db()

    with pytest.raises(ReadCategory.DoesNotExist):
        contents.read_category.refresh_from_db()

    with pytest.raises(ReadThread.DoesNotExist):
        contents.read_thread.refresh_from_db()

    with pytest.raises(RoleCategoryACL.DoesNotExist):
        contents.category_role.refresh_from_db()

    with pytest.raises(Subscription.DoesNotExist):
        contents.subscription.refresh_from_db()

    with pytest.raises(Thread.DoesNotExist):
        contents.thread.refresh_from_db()

    with pytest.raises(WatchedThread.DoesNotExist):
        contents.watched_thread.refresh_from_db()


def assert_category_contents_moved(contents: CategoryContents, new_category: Category):
    contents.attachment.refresh_from_db()
    assert contents.attachment.category_id == new_category.id
    assert not contents.attachment.is_deleted

    with pytest.raises(CategoryGroupPermission.DoesNotExist):
        contents.category_group_permission.refresh_from_db()

    contents.legacy_attachment.refresh_from_db()
    assert contents.legacy_attachment.post_id is not None

    contents.notification.refresh_from_db()
    assert contents.notification.category_id == new_category.id

    contents.poll.refresh_from_db()
    assert contents.notification.category_id == new_category.id

    contents.poll_vote.refresh_from_db()
    assert contents.poll_vote.category_id == new_category.id

    contents.post.refresh_from_db()
    assert contents.post.category_id == new_category.id

    contents.post_edit.refresh_from_db()
    assert contents.post_edit.category_id == new_category.id

    contents.post_like.refresh_from_db()
    assert contents.post_like.category_id == new_category.id

    with pytest.raises(ReadCategory.DoesNotExist):
        contents.read_category.refresh_from_db()

    contents.read_thread.refresh_from_db()
    assert contents.read_thread.category_id == new_category.id

    with pytest.raises(RoleCategoryACL.DoesNotExist):
        contents.category_role.refresh_from_db()

    contents.subscription.refresh_from_db()
    assert contents.subscription.category_id == new_category.id

    contents.thread.refresh_from_db()
    assert contents.thread.category_id == new_category.id

    contents.watched_thread.refresh_from_db()
    assert contents.watched_thread.category_id == new_category.id


def test_delete_category_deletes_category_contents(
    user, other_user, members_group, default_category
):
    contents = create_category_contents(
        user, other_user, members_group, default_category
    )

    default_category.set_last_thread(contents.thread)
    default_category.save()

    delete_category(default_category)

    with pytest.raises(Category.DoesNotExist):
        default_category.refresh_from_db()

    assert_category_contents_deleted(contents)


def test_delete_category_deletes_child_category_contents(
    user, other_user, members_group, default_category
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    contents = create_category_contents(user, other_user, members_group, child_category)

    default_category.set_last_thread(contents.thread)
    default_category.save()

    delete_category(default_category, move_children_to=None)

    with pytest.raises(Category.DoesNotExist):
        default_category.refresh_from_db()

    assert_category_contents_deleted(contents)


def test_delete_category_moves_category_contents(
    user, other_user, members_group, default_category, sibling_category
):
    contents = create_category_contents(
        user, other_user, members_group, default_category
    )

    default_category.set_last_thread(contents.thread)
    default_category.save()

    delete_category(default_category, move_contents_to=sibling_category)

    with pytest.raises(Category.DoesNotExist):
        default_category.refresh_from_db()

    assert_category_contents_moved(contents, sibling_category)


def test_delete_category_moves_deleted_child_category_contents(
    user, other_user, members_group, default_category, sibling_category
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    contents = create_category_contents(user, other_user, members_group, child_category)

    default_category.set_last_thread(contents.thread)
    default_category.save()

    delete_category(
        default_category,
        move_children_to=None,
        move_contents_to=sibling_category,
    )

    with pytest.raises(Category.DoesNotExist):
        default_category.refresh_from_db()

    assert_category_contents_moved(contents, sibling_category)


# A list of parametrized test params for category deletion
DELETE_CATEGORY_TEST_CASES = {
    "case-1": (
        {
            0: None,
            1: 0,
        },
        1,
        None,
        [
            (0, None, 0, 1, 2),
        ],
    ),
    "case-2": (
        {
            0: None,
            1: 0,
            2: 0,
        },
        1,
        None,
        [
            (0, None, 0, 1, 4),
            (2, 0, 1, 2, 3),
        ],
    ),
    "case-3": (
        {
            0: None,
            1: 0,
            2: 0,
        },
        2,
        None,
        [
            (0, None, 0, 1, 4),
            (1, 0, 1, 2, 3),
        ],
    ),
    "case-4": (
        {
            0: None,
            1: 0,
            2: 0,
            3: 0,
        },
        1,
        None,
        [
            (0, None, 0, 1, 6),
            (2, 0, 1, 2, 3),
            (3, 0, 1, 4, 5),
        ],
    ),
    "case-5": (
        {
            0: None,
            1: 0,
            2: 0,
            3: 0,
        },
        2,
        None,
        [
            (0, None, 0, 1, 6),
            (1, 0, 1, 2, 3),
            (3, 0, 1, 4, 5),
        ],
    ),
    "case-6": (
        {
            0: None,
            1: 0,
            2: 0,
            3: 0,
        },
        3,
        None,
        [
            (0, None, 0, 1, 6),
            (1, 0, 1, 2, 3),
            (2, 0, 1, 4, 5),
        ],
    ),
    "case-7": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 0,
        },
        1,
        None,
        [
            (0, None, 0, 1, 4),
            (3, 0, 1, 2, 3),
        ],
    ),
    "case-8": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 0,
        },
        1,
        True,
        [
            (0, None, 0, 1, 6),
            (3, 0, 1, 2, 3),
            (2, 0, 1, 4, 5),
        ],
    ),
    "case-9": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 0,
        },
        1,
        3,
        [
            (0, None, 0, 1, 6),
            (3, 0, 1, 2, 5),
            (2, 3, 2, 3, 4),
        ],
    ),
    "case-10": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 0,
            4: 0,
        },
        1,
        None,
        [
            (0, None, 0, 1, 6),
            (3, 0, 1, 2, 3),
            (4, 0, 1, 4, 5),
        ],
    ),
    "case-11": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 0,
            4: 0,
        },
        2,
        None,
        [
            (0, None, 0, 1, 8),
            (1, 0, 1, 2, 3),
            (3, 0, 1, 4, 5),
            (4, 0, 1, 6, 7),
        ],
    ),
    "case-12": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 0,
            4: 0,
        },
        3,
        None,
        [
            (0, None, 0, 1, 8),
            (1, 0, 1, 2, 5),
            (2, 1, 2, 3, 4),
            (4, 0, 1, 6, 7),
        ],
    ),
    "case-13": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 0,
            4: 0,
        },
        4,
        None,
        [
            (0, None, 0, 1, 8),
            (1, 0, 1, 2, 5),
            (2, 1, 2, 3, 4),
            (3, 0, 1, 6, 7),
        ],
    ),
    "case-14": (
        {
            0: None,
            1: 0,
            2: 0,
            3: 2,
            4: 0,
        },
        1,
        None,
        [
            (0, None, 0, 1, 8),
            (2, 0, 1, 2, 5),
            (3, 2, 2, 3, 4),
            (4, 0, 1, 6, 7),
        ],
    ),
    "case-15": (
        {
            0: None,
            1: 0,
            2: 0,
            3: 2,
            4: 0,
        },
        2,
        None,
        [
            (0, None, 0, 1, 6),
            (1, 0, 1, 2, 3),
            (4, 0, 1, 4, 5),
        ],
    ),
    "case-16": (
        {
            0: None,
            1: 0,
            2: 0,
            3: 2,
            4: 0,
        },
        3,
        None,
        [
            (0, None, 0, 1, 8),
            (1, 0, 1, 2, 3),
            (2, 0, 1, 4, 5),
            (4, 0, 1, 6, 7),
        ],
    ),
    "case-17": (
        {
            0: None,
            1: 0,
            2: 0,
            3: 2,
            4: 0,
        },
        4,
        None,
        [
            (0, None, 0, 1, 8),
            (1, 0, 1, 2, 3),
            (2, 0, 1, 4, 7),
            (3, 2, 2, 5, 6),
        ],
    ),
    "case-18": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 2,
            4: 0,
        },
        2,
        None,
        [
            (0, None, 0, 1, 6),
            (1, 0, 1, 2, 3),
            (4, 0, 1, 4, 5),
        ],
    ),
    "case-19": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 2,
            4: 0,
        },
        2,
        True,
        [
            (0, None, 0, 1, 8),
            (1, 0, 1, 2, 3),
            (4, 0, 1, 4, 5),
            (3, 0, 1, 6, 7),
        ],
    ),
    "case-20": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 2,
            4: 0,
        },
        2,
        1,
        [
            (0, None, 0, 1, 8),
            (1, 0, 1, 2, 5),
            (3, 1, 2, 3, 4),
            (4, 0, 1, 6, 7),
        ],
    ),
    "case-21": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 2,
            4: 0,
        },
        2,
        4,
        [
            (0, None, 0, 1, 8),
            (1, 0, 1, 2, 3),
            (4, 0, 1, 4, 7),
            (3, 4, 2, 5, 6),
        ],
    ),
    "case-22": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 2,
            4: 3,
            5: 0,
        },
        2,
        None,
        [
            (0, None, 0, 1, 6),
            (1, 0, 1, 2, 3),
            (5, 0, 1, 4, 5),
        ],
    ),
    "case-23": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 2,
            4: 3,
            5: 0,
        },
        2,
        True,
        [
            (0, None, 0, 1, 10),
            (1, 0, 1, 2, 3),
            (5, 0, 1, 4, 5),
            (3, 0, 1, 6, 9),
            (4, 3, 2, 7, 8),
        ],
    ),
    "case-24": (
        {
            0: None,
            1: 0,
            2: 1,
            3: 2,
            4: 3,
            5: 0,
        },
        2,
        1,
        [
            (0, None, 0, 1, 10),
            (1, 0, 1, 2, 7),
            (3, 1, 2, 3, 6),
            (4, 3, 3, 4, 5),
            (5, 0, 1, 8, 9),
        ],
    ),
}


@pytest.mark.parametrize(
    "tree,delete,move_to,valid_tree",
    DELETE_CATEGORY_TEST_CASES.values(),
    ids=DELETE_CATEGORY_TEST_CASES,
)
def test_delete_category_maintains_valid_category_tree(
    root_category, tree, delete, move_to, valid_tree
):
    Category.objects.filter(tree_id=root_category.tree_id, level__gt=0).delete()
    categories = generate_categories_tree(root_category, tree)
    indexes = {category.id: index for index, category in categories.items()}

    if move_to is True or move_to is None:
        move_children_to = move_to
    else:
        move_children_to = categories[move_to]

    delete_category(
        categories.pop(delete),
        move_children_to=move_children_to,
    )

    tree_db = [
        (indexes[c.id], indexes.get(c.parent_id), c.level, c.lft, c.rght)
        for c in Category.objects.filter(tree_id=root_category.tree_id).order_by("lft")
    ]

    assert tree_db == valid_tree


def generate_categories_tree(
    root_category: Category, tree: dict[int, int]
) -> dict[int, Category]:
    categories: dict[int, Category] = {0: root_category}
    for category_id, category_parent in tree.items():
        if category_id == 0:
            continue

        parent = categories[category_parent]
        categories[category_id] = Category.objects.create(
            name=f"Category #{category_id}",
            slug=f"category-{category_id}",
            parent=parent,
            tree_id=parent.tree_id,
            level=parent.level + 1,
        )

    heal_category_trees()

    queryset = Category.objects.filter(tree_id=root_category.tree_id).order_by("lft")
    return {i: category for i, category in enumerate(queryset)}
