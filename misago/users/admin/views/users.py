from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import pgettext, pgettext_lazy
from django.views.decorators.debug import sensitive_post_parameters

from ....acl.useracl import get_user_acl
from ....admin.auth import authorize_admin
from ....admin.views import generic
from ....core.mail import mail_users
from ...avatars.dynamic import set_avatar as set_dynamic_avatar
from ...datadownloads import request_user_data_download, user_has_data_download_request
from ...deletesrecord import record_user_deleted_by_staff
from ...models import Ban
from ...profilefields import profilefields
from ...setupnewuser import setup_new_user
from ...signatures import set_user_signature
from ..forms.users import (
    BanUsersForm,
    EditUserForm,
    NewUserForm,
    create_filter_users_form,
    user_form_factory,
)
from ..tasks import delete_user_with_content

User = get_user_model()


class UserAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:users:index"
    templates_dir = "misago/admin/users"
    model = User

    def get_form_class(self, request, target):
        return user_form_factory(self.form_class, target)


class UsersList(UserAdmin, generic.ListView):
    items_per_page = 24
    ordering = [
        ("-id", pgettext_lazy("admin users ordering choice", "From newest")),
        ("id", pgettext_lazy("admin users ordering choice", "From oldest")),
        ("slug", pgettext_lazy("admin users ordering choice", "A to z")),
        ("-slug", pgettext_lazy("admin users ordering choice", "Z to a")),
        ("-posts", pgettext_lazy("admin users ordering choice", "Biggest posters")),
        ("posts", pgettext_lazy("admin users ordering choice", "Smallest posters")),
    ]
    selection_label = pgettext_lazy("admin users", "With users: 0")
    empty_selection_label = pgettext_lazy("admin users", "Select users")
    mass_actions = [
        {
            "action": "activate",
            "name": pgettext_lazy("admin users", "Activate accounts"),
        },
        {
            "action": "ban",
            "name": pgettext_lazy("admin users", "Ban users"),
            "icon": "fa fa-lock",
        },
        {
            "action": "request_data_download",
            "name": pgettext_lazy("admin users", "Request data download"),
        },
        {
            "action": "delete_accounts",
            "name": pgettext_lazy("admin users", "Delete accounts"),
            "confirmation": pgettext_lazy(
                "admin users", "Are you sure you want to delete selected users?"
            ),
        },
        {
            "action": "delete_all",
            "name": pgettext_lazy("admin users", "Delete with content"),
            "confirmation": pgettext_lazy(
                "admin users",
                "Are you sure you want to delete selected users? This will also delete all content associated with their accounts.",
            ),
            "is_atomic": False,
        },
    ]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.prefetch_related("rank", "group")

    def get_filter_form(self, request):
        return create_filter_users_form()

    def action_activate(self, request, users):
        inactive_users = []
        for user in users:
            if user.requires_activation:
                inactive_users.append(user)

        if not inactive_users:
            message = pgettext("admin users", "You have to select inactive users.")
            raise generic.MassActionError(message)
        else:
            activated_users_pks = [u.pk for u in inactive_users]
            queryset = User.objects.filter(pk__in=activated_users_pks)
            queryset.update(requires_activation=User.ACTIVATION_NONE)

            subject = pgettext(
                "account activated email subject",
                "Your account on %(forum_name)s forums has been activated",
            )
            mail_subject = subject % {"forum_name": request.settings.forum_name}

            mail_users(
                inactive_users,
                mail_subject,
                "misago/emails/activation/by_admin",
                context={"settings": request.settings},
            )

            messages.success(
                request,
                pgettext("admin users", "Selected users accounts have been activated."),
            )

    def action_ban(
        self, request, users
    ):  # pylint: disable=too-many-locals, too-many-nested-blocks, too-many-branches
        users = users.order_by("slug")
        for user in users:
            if user.is_staff:
                message = pgettext(
                    "admin users", "%(user)s is admin and can't be banned."
                )
                mesage = message % {"user": user.username}
                raise generic.MassActionError(mesage)

        form = BanUsersForm(users=users)
        if "finalize" in request.POST:
            form = BanUsersForm(request.POST, users=users)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                banned_values = []

                ban_kwargs = {
                    "user_message": cleaned_data.get("user_message"),
                    "staff_message": cleaned_data.get("staff_message"),
                    "expires_on": cleaned_data.get("expires_on"),
                }

                for user in users:
                    for ban in cleaned_data["ban_type"]:
                        banned_value = None

                        if ban == "usernames":
                            check_type = Ban.USERNAME
                            banned_value = user.username.lower()

                        if ban == "emails":
                            check_type = Ban.EMAIL
                            banned_value = user.email.lower()

                        if ban == "domains":
                            check_type = Ban.EMAIL
                            banned_value = user.email.lower()
                            at_pos = banned_value.find("@")
                            banned_value = "*%s" % banned_value[at_pos:]

                        if ban == "ip" and user.joined_from_ip:
                            check_type = Ban.IP
                            banned_value = user.joined_from_ip

                        if ban in ("ip_first", "ip_two") and user.joined_from_ip:
                            check_type = Ban.IP

                            if ":" in user.joined_from_ip:
                                ip_separator = ":"
                            if "." in user.joined_from_ip:
                                ip_separator = "."

                            bits = user.joined_from_ip.split(ip_separator)
                            if ban == "ip_first":
                                formats = (bits[0], ip_separator)
                            if ban == "ip_two":
                                formats = (bits[0], ip_separator, bits[1], ip_separator)
                            banned_value = "%s*" % ("".join(formats))

                        if banned_value and banned_value not in banned_values:
                            ban_kwargs.update(
                                {"check_type": check_type, "banned_value": banned_value}
                            )
                            Ban.objects.create(**ban_kwargs)
                            banned_values.append(banned_value)

                Ban.objects.invalidate_cache()
                messages.success(
                    request, pgettext("admin users", "Selected users have been banned.")
                )
                return None

        return self.render(
            request,
            {"users": users, "form": form},
            template_name="misago/admin/users/ban.html",
        )

    def action_request_data_download(self, request, users):
        for user in users:
            if not user_has_data_download_request(user):
                request_user_data_download(user, requester=request.user)

        messages.success(
            request,
            pgettext(
                "admin users",
                "Data download requests have been placed for selected users.",
            ),
        )

    def action_delete_accounts(self, request, users):
        for user in users:
            if user == request.user:
                raise generic.MassActionError(
                    pgettext("admin users", "You can't delete yourself.")
                )
            if user.is_misago_admin:
                raise generic.MassActionError(
                    pgettext(
                        "admin users",
                        "%(user)s can't be deleted because they are a Misago administrator.",
                    )
                    % {"user": user.username}
                )
            if user.is_staff:
                raise generic.MassActionError(
                    pgettext(
                        "admin users",
                        "%(user)s can't be deleted because they are a Django staff.",
                    )
                    % {"user": user.username}
                )

        for user in users:
            user.delete(anonymous_username=request.settings.anonymous_username)
            record_user_deleted_by_staff()

        messages.success(
            request, pgettext("admin users", "Selected users have been deleted.")
        )

    def action_delete_all(self, request, users):
        for user in users:
            if user == request.user:
                raise generic.MassActionError(
                    pgettext("admin users", "You can't delete yourself.")
                )
            if user.is_misago_admin:
                raise generic.MassActionError(
                    pgettext(
                        "admin users",
                        "%(user)s can't be deleted because they are a Misago administrator.",
                    )
                    % {"user": user.username}
                )
            if user.is_staff:
                raise generic.MassActionError(
                    pgettext(
                        "admin users",
                        "%(user)s can't be deleted because they are a Django staff.",
                    )
                    % {"user": user.username}
                )

        for user in users:
            user.is_active = False
            user.save()

            delete_user_with_content.delay(user.pk)

        messages.success(
            request,
            pgettext(
                "admin users",
                "Selected users have been disabled and queued for deletion together with their content.",
            ),
        )


class NewUser(UserAdmin, generic.ModelFormView):
    form_class = NewUserForm
    template_name = "new.html"
    message_submit = pgettext_lazy(
        "admin users", 'New user "%(user)s" has been registered.'
    )

    @method_decorator(sensitive_post_parameters("new_password"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class, request, target):
        if request.method == "POST":
            return form_class(
                request.POST, request.FILES, instance=target, request=request
            )
        return form_class(instance=target, request=request)

    def handle_form(self, form, request, target):
        new_user = User.objects.create_user(
            form.cleaned_data["username"],
            form.cleaned_data["email"],
            form.cleaned_data["new_password"],
            group=form.cleaned_data["group"],
            secondary_groups=form.cleaned_data["secondary_groups"],
            title=form.cleaned_data["title"],
            rank=form.cleaned_data.get("rank"),
            joined_from_ip=request.user_ip,
        )

        if form.cleaned_data.get("roles"):
            new_user.roles.add(*form.cleaned_data["roles"])

        new_user.update_acl_key()
        setup_new_user(request.settings, new_user)

        messages.success(request, self.message_submit % {"user": target.username})
        return redirect("misago:admin:users:edit", pk=new_user.pk)


class EditUser(UserAdmin, generic.ModelFormView):
    form_class = EditUserForm
    template_name = "edit.html"
    message_submit = pgettext_lazy("admin users", 'User "%(user)s" has been edited.')

    @method_decorator(sensitive_post_parameters("new_password"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def real_dispatch(self, request, target):
        target.old_username = target.username
        target.old_is_avatar_locked = target.is_avatar_locked
        return super().real_dispatch(request, target)

    def get_form(self, form_class, request, target):
        if request.method == "POST":
            return form_class(
                request.POST, request.FILES, instance=target, request=request
            )
        return form_class(instance=target, request=request)

    def handle_form(self, form, request, target):
        target.username = target.old_username
        if target.username != form.cleaned_data["username"]:
            target.set_username(form.cleaned_data["username"], changed_by=request.user)

        if form.cleaned_data.get("new_password"):
            target.set_password(form.cleaned_data["new_password"])

        if form.cleaned_data.get("email"):
            target.set_email(form.cleaned_data["email"])

        if form.cleaned_data.get("is_avatar_locked"):
            if not target.old_is_avatar_locked:
                set_dynamic_avatar(target)

        if not form.fields["is_misago_root"].disabled:
            target.is_misago_root = form.cleaned_data["is_misago_root"]

        if not form.fields["is_active"].disabled:
            target.is_active = form.cleaned_data["is_active"]
        if not form.fields["is_active_staff_message"].disabled:
            target.is_active_staff_message = form.cleaned_data.get(
                "is_active_staff_message"
            )

        target.set_groups(
            form.cleaned_data["group"],
            form.cleaned_data["secondary_groups"],
        )

        target.rank = form.cleaned_data.get("rank")

        target.roles.clear()
        target.roles.add(*form.cleaned_data["roles"])

        target_acl = get_user_acl(target, request.cache_versions)
        set_user_signature(
            request, target, target_acl, form.cleaned_data.get("signature")
        )

        profilefields.update_user_profile_fields(request, target, form)

        target.update_acl_key()
        target.save()

        if target.pk == request.user.pk:
            authorize_admin(request)
            update_session_auth_hash(request, target)

        messages.success(request, self.message_submit % {"user": target.username})
