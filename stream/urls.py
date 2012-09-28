from django.conf.urls import patterns, url

urlpatterns = patterns('stream.views',
    #url(r'^$', 'index'),
    url(r'^$', 'test'),
    url(r'^stream/$', 'stream'),
    url(r'^post/(?P<post_id>\d+)/$', 'view_post'),
    url(r'^thread/(?P<thread_id>\d+)/$', 'view_thread'),
)

urlpatterns += patterns('stream.ajax',
    url(r'^api/post/get/$', 'api_get_posts'),
    url(r'^api/post/new/$', 'api_new_post'),
    url(r'^api/post/re/$', 'api_reply_post'),
    url(r'^api/post/pu/$', 'api_push_post'),

    url(r'^api/push/get/$', 'api_get_pushes'),

    url(r'^api/tag/add/$', 'api_add_tag'),
    url(r'^api/tag/vote/$', 'api_vote_live_tag'),
)