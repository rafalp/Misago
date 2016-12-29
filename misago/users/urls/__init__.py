from django.conf.urls import include, url

from misago.core.views import home_redirect

from ..views import activation, auth, forgottenpassword, lists, options, profile


urlpatterns = [
    url(r'^banned/$', home_redirect, name='banned'),

    url(r'^login/$', auth.login, name='login'),
    url(r'^logout/$', auth.logout, name='logout'),

    url(r'^request-activation/$', activation.request_activation, name='request-activation'),
    url(r'^activation/(?P<pk>\d+)/(?P<token>[a-zA-Z0-9]+)/$', activation.activate_by_token, name='activate-by-token'),

    url(r'^forgotten-password/$', forgottenpassword.request_reset, name='forgotten-password'),
    url(r'^forgotten-password/(?P<pk>\d+)/(?P<token>[a-zA-Z0-9]+)/$', forgottenpassword.reset_password_form, name='forgotten-password-change-form'),
]


urlpatterns += [
    url(r'^options/$', options.index, name='options'),
    url(r'^options/(?P<form_name>[-a-zA-Z]+)/$', options.index, name='options-form'),

    url(r'^options/forum-options/$', options.index, name='usercp-change-forum-options'),
    url(r'^options/change-username/$', options.index, name='usercp-change-username'),
    url(r'^options/sign-in-credentials/$', options.index, name='usercp-change-email-password'),

    url(r'^options/change-email/(?P<token>[a-zA-Z0-9]+)/$', options.confirm_email_change, name='options-confirm-email-change'),
    url(r'^options/change-password/(?P<token>[a-zA-Z0-9]+)/$', options.confirm_password_change, name='options-confirm-password-change'),
]


urlpatterns += [
    url(r'^users/', include([
        url(r'^$', lists.landing, name='users'),
        url(r'^active-posters/$', lists.active_posters, name='users-active-posters'),
        url(r'^(?P<slug>[-a-zA-Z0-9]+)/$', lists.rank, name='users-rank'),
        url(r'^(?P<slug>[-a-zA-Z0-9]+)/(?P<page>\d+)/$', lists.rank, name='users-rank'),
    ]))
]


urlpatterns += [
    url(r'^u/(?P<slug>[a-zA-Z0-9]+)/(?P<pk>\d+)/', include([
        url(r'^$', profile.landing, name='user'),
        url(r'^posts/$', profile.posts, name='user-posts'),
        url(r'^threads/$', profile.threads, name='user-threads'),
        url(r'^followers/$', profile.followers, name='user-followers'),
        url(r'^follows/$', profile.follows, name='user-follows'),
        url(r'^username-history/$', profile.username_history, name='username-history'),
        url(r'^ban-details/$', profile.user_ban, name='user-ban'),
    ]))
]
