from ..models import Setting


def test_setting_value_is_hydrated_by_getter(db):
    setting = Setting(python_type="list", dry_value="lorem,ipsum")
    assert setting.value == ["lorem", "ipsum"]


def test_setting_value_is_dehydrated_by_setter(db):
    setting = Setting(python_type="list")
    setting.value = ["lorem", "ipsum"]
    assert setting.dry_value == "lorem,ipsum"


def test_setting_value_is_set_to_none(db):
    setting = Setting(python_type="list", dry_value="lorem,ipsum")
    setting.value = None
    assert setting.dry_value is None
