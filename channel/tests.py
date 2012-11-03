from channel.models import *

class ChannelTest(object):
    """
>>> u, c = User.objects.get_or_create(username='uuu1', password='uuu1')
>>> n = NounTag.objects.get_or_create(name="aaa", user=u)
>>> n = NounTag.objects.get_or_create(name="bbb", user=u)
>>> n = NounTag.objects.get_or_create(name="ccc", user=u)

# testing channel model
>>> c = Channel.objects.create(user=u)
>>> c.add_tag("aaa")
>>> c
<Channel: uuu1:[<NounTag: NNT|aaa>]>
>>> c.remove_tag("aaa")
>>> c
<Channel: uuu1:[]>
>>> c.add_tag("aaa")
>>> c.add_tag("bbb")
>>> c.add_tag("ccc")
>>> c.to_json()
{'tags': [u'aaa', u'bbb', u'ccc'], 'id': 1, 'name': u'channel'}
    """