from django.conf.urls import patterns, url

urlpatterns = patterns('channel.ajax',
    # actions of tagcanal
    url(r'^api/cha/get/$', 'get_channels'),
    url(r'^api/cha/new/$', 'new_channel'),
    url(r'^api/cha/tag/$', 'tag_channel'),
)