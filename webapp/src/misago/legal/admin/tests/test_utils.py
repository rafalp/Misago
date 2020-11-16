from ...models import Agreement, UserAgreement
from ..utils import disable_agreement, set_agreement_as_active


def test_activating_inactive_agreement_updates_its_flag_but_doesnt_commit_to_db(db):
    agreement = Agreement.objects.create(
        type=Agreement.TYPE_PRIVACY, link="https://somewhre.com", text="Lorem ipsum"
    )

    set_agreement_as_active(agreement)
    assert agreement.is_active

    agreement.refresh_from_db()
    assert not agreement.is_active


def test_activating_inactive_agreement_with_commit_updates_its_flag_in_db(db):
    agreement = Agreement.objects.create(
        type=Agreement.TYPE_PRIVACY, link="https://somewhre.com", text="Lorem ipsum"
    )

    set_agreement_as_active(agreement, commit=True)
    assert agreement.is_active

    agreement.refresh_from_db()
    assert agreement.is_active


def test_activating_agreement_deactivates_other_active_agreement_of_same_type(db):
    old_agreement = Agreement.objects.create(
        type=Agreement.TYPE_PRIVACY,
        link="https://somewhre.com",
        text="Lorem ipsum",
        is_active=True,
    )

    new_agreement = Agreement.objects.create(
        type=Agreement.TYPE_PRIVACY, link="https://somewhre.com", text="Lorem ipsum"
    )

    set_agreement_as_active(new_agreement, commit=True)

    old_agreement.refresh_from_db()
    new_agreement.refresh_from_db()

    assert not old_agreement.is_active
    assert new_agreement.is_active


def test_activating_agreement_doesnt_deactivate_agreement_of_other_type(db):
    agreement = Agreement.objects.create(
        type=Agreement.TYPE_PRIVACY, link="https://somewhre.com", text="Lorem ipsum"
    )

    other_type_agreement = Agreement.objects.create(
        type=Agreement.TYPE_TOS,
        link="https://somewhre.com",
        text="Lorem ipsum",
        is_active=True,
    )

    set_agreement_as_active(agreement, commit=True)

    agreement.refresh_from_db()
    other_type_agreement.refresh_from_db()

    assert agreement.is_active
    assert other_type_agreement.is_active


def test_disabling_active_agreement_updates_its_flag_but_doesnt_commit_to_db(db):
    agreement = Agreement.objects.create(
        type=Agreement.TYPE_PRIVACY,
        link="https://somewhre.com",
        text="Lorem ipsum",
        is_active=True,
    )

    disable_agreement(agreement)
    assert not agreement.is_active

    agreement.refresh_from_db()
    assert agreement.is_active


def test_disabling_active_agreement_with_commit_updates_its_flag_in_db(db):
    agreement = Agreement.objects.create(
        type=Agreement.TYPE_PRIVACY,
        link="https://somewhre.com",
        text="Lorem ipsum",
        is_active=True,
    )

    disable_agreement(agreement, commit=True)
    assert not agreement.is_active

    agreement.refresh_from_db()
    assert not agreement.is_active
