from django.conf.urls import patterns, url

urlpatterns = patterns('misago.avatarcp.views',
    url(r'^avatar/$', 'avatar', name="usercp_avatar"),
    #url(r'^avatar/gallery/$', 'gallery', name="usercp_avatar_gallery"),
    #url(r'^avatar/upload/$', 'upload', name="usercp_avatar_upload"),
    #url(r'^avatar/crop/$', 'crop', name="usercp_avatar_crop"),
    #url(r'^avatar/gravatar/$', 'gravatar', name="usercp_avatar_gravatar"),
)