from django.conf.urls import patterns, include, url
from misago.threads.views.post import (QuotePostView, ApprovePostView,
                                       HidePostView, UnhidePostView,
                                       DeletePostView)


urlpatterns = patterns('',
    url(r'^post/(?P<post_id>\d+)/quote/$', QuotePostView.as_view(), name='quote_post'),
    url(r'^post/(?P<post_id>\d+)/approve/$', ApprovePostView.as_view(), name='approve_post'),
    url(r'^post/(?P<post_id>\d+)/unhide/$', UnhidePostView.as_view(), name='unhide_post'),
    url(r'^post/(?P<post_id>\d+)/hide/$', HidePostView.as_view(), name='hide_post'),
    url(r'^post/(?P<post_id>\d+)/delete/$', DeletePostView.as_view(), name='delete_post'),
)
