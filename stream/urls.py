from django.conf.urls import patterns, url

urlpatterns = patterns('stream.views',
    #url(r'^$', 'index'),
    url(r'^$', 'test'),
    url(r'^stream/$', 'stream'),
    url(r'^post/(?P<post_id>\d+)/$', 'view_post'),
    url(r'^thread/(?P<thread_id>\d+)/$', 'view_thread'),
)

urlpatterns += patterns('stream.ajax',
    # actions of post
    url(r'^api/post/get/$', 'get_posts'),
    url(r'^api/post/new/$', 'new_post'),
    url(r'^api/post/re/$', 'reply_post'),
    url(r'^api/post/pu/$', 'push_post'),
    url(r'^api/post/tag/$', 'tag_post'),
    # actions of push
    url(r'^api/push/get/$', 'get_pushes'),
    # actions of tag
    url(r'^api/tag/vote/$', 'vote_live_tag'),
    # actions of channel
    url(r'^api/cha/get/$', 'get_channels'),
    url(r'^api/cha/new/$', 'new_channel'),
    url(r'^api/cha/tag/$', 'tag_channel'),
    # actions of thread
)