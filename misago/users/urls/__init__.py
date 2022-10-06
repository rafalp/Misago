from django.urls import include, path

from ...core.views import home_redirect

from ..views import (
    activation,
    auth,
    avatarserver,
    forgottenpassword,
    lists,
    options,
    profile,
)

urlpatterns = [
    path("banned/", home_redirect, name="banned"),
    path("login/", auth.login, name="login"),
    path("logout/", auth.logout, name="logout"),
    path(
        "request-activation/",
        activation.request_activation,
        name="request-activation",
    ),
    path(
        "activation/<int:pk>/<slug:token>/",
        activation.activate_by_token,
        name="activate-by-token",
    ),
    path(
        "forgotten-password/",
        forgottenpassword.request_reset,
        name="forgotten-password",
    ),
    path(
        "forgotten-password/<int:pk>/<slug:token>/",
        forgottenpassword.reset_password_form,
        name="forgotten-password-change-form",
    ),
]

urlpatterns += [
    path("options/", options.index, name="options"),
    path("options/<slug:form_name>/", options.index, name="options-form"),
    path("options/forum-options/", options.index, name="usercp-change-forum-options"),
    path("options/edit-details/", options.index, name="usercp-edit-details"),
    path("options/change-username/", options.index, name="usercp-change-username"),
    path(
        "options/sign-in-credentials/",
        options.index,
        name="usercp-change-email-password",
    ),
    path(
        "options/change-email/<slug:token>/",
        options.confirm_email_change,
        name="options-confirm-email-change",
    ),
    path(
        "options/change-password/<slug:token>/",
        options.confirm_password_change,
        name="options-confirm-password-change",
    ),
    path("options/dowload-data/", options.index, name="usercp-download-data"),
    path("options/delete-account/", options.index, name="usercp-delete-account"),
]

urlpatterns += [
    path(
        "users/",
        include(
            [
                path("", lists.landing, name="users"),
                path(
                    "active-posters/",
                    lists.ActivePostersView.as_view(),
                    name="users-active-posters",
                ),
                path(
                    "<slug:slug>/",
                    lists.RankUsersView.as_view(),
                    name="users-rank",
                ),
                path(
                    "<slug:slug>/<int:page>/",
                    lists.RankUsersView.as_view(),
                    name="users-rank",
                ),
            ]
        ),
    )
]

urlpatterns += [
    path(
        "u/<slug:slug>/<int:pk>/",
        include(
            [
                path("", profile.LandingView.as_view(), name="user"),
                path("posts/", profile.UserPostsView.as_view(), name="user-posts"),
                path(
                    "threads/",
                    profile.UserThreadsView.as_view(),
                    name="user-threads",
                ),
                path(
                    "followers/",
                    profile.UserFollowersView.as_view(),
                    name="user-followers",
                ),
                path(
                    "follows/",
                    profile.UserFollowsView.as_view(),
                    name="user-follows",
                ),
                path(
                    "details/",
                    profile.UserProfileDetailsView.as_view(),
                    name="user-details",
                ),
                path(
                    "username-history/",
                    profile.UserUsernameHistoryView.as_view(),
                    name="username-history",
                ),
                path("ban-details/", profile.UserBanView.as_view(), name="user-ban"),
            ]
        ),
    )
]

urlpatterns += [
    path("avatar/", avatarserver.blank_avatar, name="blank-avatar"),
    path(
        "avatar/<int:pk>/<int:size>/",
        avatarserver.user_avatar,
        name="user-avatar",
    ),
]
