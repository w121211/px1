from django.conf.urls import patterns, url

urlpatterns = patterns('forum.views',
    url(r'^$', 'main'),
    url(r'^forum/(\d+)/$', 'forum'),
    url(r'^forum/thread/(\d+)/$', 'thread'),
    url(r'^post/(new_thread|reply)/(\d+)/$', 'post'),
    url(r'^new_thread/(\d+)/$', 'new_thread'),
    url(r'^reply/(\d+)/$', 'reply')
)