from unittest.mock import ANY

from ...users.profilefields.default import GenderField, RealNameField
from ..profilefields import ProfileFieldsLoader

PROFILE_FIELDS_CONFIG = [
    {
        "name": "Fieldset",
        "fields": [
            "misago.users.profilefields.default.RealNameField",
            "misago.users.profilefields.default.GenderField",
        ],
    }
]


def test_profile_fields_loader_profile_fields_attr_returns_fields_objects():
    loader = ProfileFieldsLoader(PROFILE_FIELDS_CONFIG)

    assert len(loader.profile_fields) == 2
    assert isinstance(
        loader.profile_fields["misago.users.profilefields.default.RealNameField"],
        RealNameField,
    )
    assert isinstance(
        loader.profile_fields["misago.users.profilefields.default.GenderField"],
        GenderField,
    )


def test_profile_fields_loader_fields_dict_attr_returns_fields_objects():
    loader = ProfileFieldsLoader(PROFILE_FIELDS_CONFIG)

    assert len(loader.fields_dict) == 2
    assert isinstance(loader.fields_dict[RealNameField.fieldname], RealNameField)
    assert isinstance(loader.fields_dict[GenderField.fieldname], GenderField)


def test_profile_fields_loader_get_form_data_attr_returns_form_data_helper(user):
    loader = ProfileFieldsLoader(PROFILE_FIELDS_CONFIG)
    form_data = loader.get_form_data(None, user)

    assert form_data.fieldsets == [
        {
            "name": "Fieldset",
            "fields": [
                ANY,
                ANY,
            ],
        }
    ]
    assert form_data.fields == {
        RealNameField.fieldname: ANY,
        GenderField.fieldname: ANY,
    }
