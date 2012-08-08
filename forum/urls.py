from django.conf.urls import patterns, url

urlpatterns = patterns('forum.views',
    url(r'^$', 'index'),
    url(r'^tag/$', 'tag'),
    url(r'^tag/board$', 'tag_board'),
    url(r'^board/(\d+)/$', 'board'),
    url(r'^board/new/$', 'new_board'),
    url(r'^board/thread/(\d+)/$', 'thread'),
    url(r'^post/(new_thread|reply)/(\d+)/$', 'post'),
    url(r'^new_thread/(\d+)/$', 'new_thread'),
    url(r'^reply/(\d+)/$', 'reply'),
)