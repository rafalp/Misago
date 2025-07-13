from ..updatedobjectwrapper import UpdatedObjectWrapper


def test_updated_object_wrapper_save_returns_false_if_no_fields_were_changed(
    django_assert_num_queries, user
):
    obj = UpdatedObjectWrapper(user)

    with django_assert_num_queries(0):
        assert not obj.save()


def test_updated_object_wrapper_save_returns_true_if_field_was_changed(
    django_assert_num_queries, user
):
    obj = UpdatedObjectWrapper(user)
    obj.slug = "changed"

    with django_assert_num_queries(1):
        assert obj.save()

    assert obj._update_fields == {"slug"}


def test_updated_object_wrapper_save_returns_true_if_eager_field_was_read(
    django_assert_num_queries, user
):
    obj = UpdatedObjectWrapper(user, ("plugin_data",))
    len(obj.plugin_data)

    with django_assert_num_queries(1):
        assert obj.save()

    assert obj._update_fields == {"plugin_data"}
