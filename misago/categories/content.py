from .models import Category


def move_category_content(src: Category, dst: Category):
    _move_category_content_action(src, dst)


def _move_category_content_action(src: Category, dst: Category):
    src.readthreadset.update(category=dst)
    src.threadset.update(category=dst)
    src.postset.update(category=dst)


def delete_category_content(category: Category):
    _delete_category_content_action(category)


def _delete_category_content_action(category: Category):
    pass
