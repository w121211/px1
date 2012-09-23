from django.conf.urls import patterns, url

urlpatterns = patterns('stream.views',
    #url(r'^$', 'index'),
    url(r'^$', 'test'),
#    url(r'^stream/$', 'stream'),
    url(r'^post/(?P<post_id>\d+)/$', 'view_post'),
    url(r'^thread/(?P<thread_id>\d+)/$', 'view_thread'),

    url(r'^api/post/get/$', 'api_get_posts'),
    url(r'^api/post/new/$', 'api_new_post'),
    url(r'^api/post/re/$', 'api_reply_post'),
    url(r'^api/post/pu/$', 'api_push_post'),

    url(r'^api/push/get/$', 'api_get_pushes'),
#    url(r'^$', 'index'),
#    url(r'^tag/$', 'tag'),
#    url(r'^tag/board$', 'tag_board'),
#    url(r'^board/(\d+)/$', 'board'),
#    url(r'^board/new/$', 'new_board'),
#    url(r'^board/thread/(\d+)/$', 'thread'),
#    url(r'^post/(new_thread|reply)/(\d+)/$', 'post'),
#    url(r'^new_thread/(\d+)/$', 'new_thread'),
#    url(r'^reply/(\d+)/$', 'reply'),
)