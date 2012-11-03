from django.conf.urls import patterns, url

urlpatterns = patterns('channel.ajax',
    url(r'^api/channel/get/$', 'get_channels'),
    url(r'^api/channel/add/$', 'add_channel'),
    url(r'^api/channel/remove/$', 'remove_channel'),
    url(r'^api/channel/tag/add/$', 'add_tag'),
    url(r'^api/channel/tag/remove/$', 'remove_tag'),
)