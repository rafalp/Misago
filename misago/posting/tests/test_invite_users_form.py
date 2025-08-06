from ...permissions.proxy import UserPermissionsProxy
from ...users.bans import ban_user
from ..forms import InviteUsersForm


def test_invite_users_form_sets_request(rf, user, cache_versions, dynamic_settings):
    request = rf.get("/")
    request.settings = dynamic_settings
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    form = InviteUsersForm(request=request)
    assert form.request is request


def test_invite_users_form_sets_field_max_choices(
    rf, user, members_group, cache_versions, dynamic_settings
):
    members_group.private_thread_users_limit = 12
    members_group.save()

    request = rf.get("/")
    request.settings = dynamic_settings
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    form = InviteUsersForm(request=request)
    assert form.fields["users"].max_choices == members_group.private_thread_users_limit


def test_invite_users_form_sets_field_max_choices(
    rf, user, members_group, cache_versions, dynamic_settings
):
    members_group.private_thread_users_limit = 12
    members_group.save()

    request = rf.get("/")
    request.settings = dynamic_settings
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    form = InviteUsersForm(request=request)
    assert form.fields["users"].max_choices == members_group.private_thread_users_limit


def test_invite_users_form_validates_max_choices(
    rf,
    user,
    members_group,
    cache_versions,
    dynamic_settings,
    admin,
    moderator,
    other_user,
):
    members_group.private_thread_users_limit = 2
    members_group.save()

    request = rf.post(
        "/", {"users": [admin.username, moderator.username, other_user.username]}
    )
    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    form = InviteUsersForm(request.POST, request=request)
    assert not form.is_valid()
    assert form.errors == {"users": ["Select no more than 2 users."]}


def test_invite_users_form_fails_to_validate_if_users_data_is_empty(
    rf, user, user_permissions, cache_versions, dynamic_settings
):
    request = rf.post("/", {"users": []})
    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = user_permissions

    form = InviteUsersForm(request.POST, request=request)
    assert not form.is_valid()
    assert form.errors == {"users": ["This field is required."]}


def test_invite_users_form_fails_to_validate_if_user_invites_themselves(
    rf, user, user_permissions, cache_versions, dynamic_settings
):
    request = rf.post("/", {"users": [user.username]})
    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = user_permissions

    form = InviteUsersForm(request.POST, request=request)
    assert not form.is_valid()
    assert form.errors == {"users": ["You can't invite yourself."]}


def test_invite_users_form_excludes_user_if_other_users_are_invited(
    rf, user, other_user, user_permissions, cache_versions, dynamic_settings
):
    request = rf.post("/", {"users": [user.username, other_user.username]})
    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = user_permissions

    form = InviteUsersForm(request.POST, request=request)
    assert form.is_valid()
    assert form.cleaned_data == {"users": [other_user]}


def test_invite_users_form_validates_nonexisting_users(
    rf, user, user_permissions, cache_versions, dynamic_settings
):
    request = rf.post("/", {"users": ["NotFound"]})
    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = user_permissions

    form = InviteUsersForm(request.POST, request=request)
    assert not form.is_valid()
    assert form.errors == {"users": ["One or more users not found: NotFound"]}


def test_invite_users_form_validates_deactivated_users(
    rf, user, user_permissions, cache_versions, dynamic_settings, inactive_user
):
    request = rf.post("/", {"users": [inactive_user.username]})
    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = user_permissions

    form = InviteUsersForm(request.POST, request=request)
    assert not form.is_valid()
    assert form.errors == {"users": ["One or more users not found: Inactive_User"]}


def test_invite_users_form_validates_users(
    rf, user, user_permissions, cache_versions, dynamic_settings, other_user
):
    ban_user(other_user)

    request = rf.post("/", {"users": [other_user.username]})
    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = user_permissions

    form = InviteUsersForm(request.POST, request=request)
    assert not form.is_valid()
    assert form.errors == {"users": ["Other_User: This user is banned."]}


def test_invite_users_form_prioritizes_noscript_value_if_present(
    rf, user, user_permissions, cache_versions, dynamic_settings, admin, moderator
):
    request = rf.post(
        "/", {"users": [admin.username], "users_noscript": moderator.username}
    )
    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = user_permissions

    form = InviteUsersForm(request.POST, request=request)
    assert form.is_valid()
    assert form.cleaned_data == {"users": [moderator]}
