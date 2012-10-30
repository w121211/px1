"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from tagcanal.models import *
from stream.models import *

class ModelTest(object):
    """
    # test basic models
    >>> f = {'title': 'ttt', 'body': 'bbb'}
    >>> f = PostForm(f)
    >>> po1 = f.save(commit=False)
    >>> u = User.objects.create_user(username='uuu1', password='uuu1')
    >>> po1.user = u
    >>> po1.save()
    >>> po1.to_json(u)
    {'body': 'bbb', 'title': 'ttt', 'tags': [], 'reid': None, 'user': 'uuu1', 'time': '2012-09-29T16:45:45', 'id': 1}
    >>> pu1 = Push.objects.create(user=u, body='bb', post=po1)

    # test tagging
    >>> from tagcanal.utils import GeneralTagger
    >>> g = GeneralTagger()
    >>> l = g.like.tag(po1)
    >>> l = g.noun.tag(po1, 'test', u)
    >>> l = g.like.tag(pu1)
    >>> pu1.to_json(u)
    {'body': 'bb', 'user': 'uuu1', 'tags': [{'myvote': False, 'votes': 0, 'type': u'FN', 'id': 3, 'name': u'like'}]}
    >>> po1.to_json(u)
    {'body': 'bbb', 'title': 'ttt', 'tags': [{'myvote': False, 'votes': 0, 'type': u'FN', 'id': 1, 'name': u'like'}, {'myvote': True, 'votes': 1, 'type': u'NN', 'id': 2, 'name': u'test'}], 'reid': None, 'user': 'uuu1', 'time': '2012-09-29T16:49:13', 'id': 1}

    # test channel

    """