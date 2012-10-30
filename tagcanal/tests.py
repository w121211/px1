"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import unittest
from django.db import models

from tagcanal.models import *
from tagcanal.utils import *

class TaggerBasicTest(object):
    def setUp(self):
        # create users
        self.ua, c = User.objects.get_or_create(username='autorobo', password='autorobo')
        self.u1, c = User.objects.get_or_create(username='uuu1', password='uuu1')
        self.u2, c = User.objects.get_or_create(username='uuu2', password='uuu2')

        # create tags
        self.f_like, c  = FunctionTag.objects.get_or_create(user=self.ua, name='like')
        self.n_test, c  = NounTag.objects.get_or_create(user=self.ua, name='test', sub_type='T')
        self.n_alpha, c = NounTag.objects.get_or_create(user=self.ua, name='alpha', sub_type='T')
        self.v_chat, c  = VerbTag.objects.get_or_create(user=self.ua, name='chat')
        self.v_ask, c   = VerbTag.objects.get_or_create(user=self.ua, name='ask')

        # create posts
        self.p1, c = Post.objects.get_or_create(user=self.u1)   # for tag test

        self.tagger = GeneralTagger()

    def test_base(self):
        p = Post.objects.get(user__username='uuu1')
        self.assertEqual(p, self.p1)

    def test_tag_like(self):
        t = self.tagger.like.tag(self.p1)
        self.assertIn(t, self.p1.tags.all())
        self.assertEqual(t.tag.functiontag, self.f_like)

    def test_tag_noun(self):
        t = self.tagger.noun.tag(self.p1, self.n_test, self.u1) # return a live tag
        self.assertIn(t, self.p1.tags.all())
        self.assertIn(self.u1, t.voters.all())  # tagger is in voters?
        print t.tag.type
        print t.tag.nountag.sub_type
        self.assertEqual(t.tag.nountag, self.n_test)

    def test_tag_new_noun(self):
        t = self.tagger.noun.tag(self.p1, 'aaa', self.u1) # return a live tag
        self.assertEqual(t.user, self.u1)
        self.assertEquals(t.tag.name, 'aaa')
        self.assertEquals(t.tag.type, 'NN')
        self.assertEqual(t.tag.user, self.u1)

class TaggerSearchTest(object):
    def setUp(self):
        # create users
        self.ua, c = User.objects.get_or_create(username='autorobo', password='autorobo')
        self.u1, c = User.objects.get_or_create(username='uuu1', password='uuu1')
        self.u2, c = User.objects.get_or_create(username='uuu2', password='uuu2')

        # create tags
        self.n_test, c  = NounTag.objects.get_or_create(user=self.ua, name='test', sub_type='T')
        self.n_alpha, c = NounTag.objects.get_or_create(user=self.ua, name='alpha', sub_type='T')
        self.v_chat, c  = VerbTag.objects.get_or_create(user=self.ua, name='chat')

        # create posts
        self.p1 = Post.objects.create(user=self.u1)
        self.p2 = Post.objects.create(user=self.u2)
        self.p3 = Post.objects.create(user=self.u2)
        self.p4 = Post.objects.create(user=self.u2)

        tagger = self.tagger = GeneralTagger()

        tagger.like.tag(self.p1)
        tagger.noun.tag(self.p1, self.n_test, self.u1)
        tagger.like.tag(self.p2)
        tagger.noun.tag(self.p2, self.n_test, self.u2)
        tagger.like.tag(self.p3)
        tagger.noun.tag(self.p3, self.n_alpha, self.u1)
        tagger.like.tag(self.p4)
        tagger.noun.tag(self.p4, self.n_alpha, self.u2)

    def test_search_by_nouns(self):
        '''
        '''
        qs = self.tagger.search(Post.objects.filter(), ['test'])
        print Post.objects.all()
        print self.p1.tags.all()
        print qs
        self.assertListEqual(list(qs), [self.p1, self.p2])

    def test_search_by_like(self):
        pass

    def test_search_by_nouns_and_like(self):
        pass

class TaggerTest(object):
    """
>>> u, c = User.objects.get_or_create(username='uuu1', password='uuu1')
>>> u
<User: uuu1>

>>> Item.objects.all()
[]

# init data
>>> i = Item.objects.create(user=u)
>>> i
<Item: 1:[]>

# test basic noun tagger
>>> n = NounTagger()
>>> n.tag(i, 'test', u)
<LiveTag: test>
>>> i
<Item: 1:[<LiveTag: test>]>
>>> i.tags.all()[0].tag
<Tag: NN|test>
>>> i.tags.all()[0].voters.all()
[<User: uuu1>]
>>> n.search(Item.objects.all(), ['test'])
[<Item: 1:[<LiveTag: test>]>]

# test basic like tagger
>>> l = LikeTagger('like')
>>> l0 = l.tag(i)
>>> l0.tag
<FunctionTag: FN|like>
>>> i
<Item: 1:[<LiveTag: test>, <LiveTag: like>]>
>>> i.tags.all()[0].voters.all()
[<User: uuu1>]
>>> l.search(Item.objects.filter(), u)
[]

# init data
>>> u1, c = User.objects.get_or_create(username='uuu1', password='uuu1')
>>> u2, c = User.objects.get_or_create(username='uuu2', password='uuu2')
>>> i2 = Item.objects.create(user=u1)
>>> i3 = Item.objects.create(user=u2)

# test general tagger
>>> g = GeneralTagger()
>>> l1 = g.like.tag(i2)
>>> l2 = g.noun.tag(i2, 'test', u1)
>>> l3 = g.noun.tag(i2, 'alpha', u2)
>>> l4 = g.like.tag(i3)
>>> l5 = g.noun.tag(i3, 'test', u1)
>>> l6 = g.noun.tag(i3, 'alpha', u1)

>>> l = g.vote(l0.id, u1)
>>> l = g.vote(l1.id, u1)
>>> l.voters.all()
[<User: uuu1>]
>>> l = g.vote(l2.id, u2)
>>> l.voters.all()
[<User: uuu1>, <User: uuu2>]
>>> l = g.vote(l4.id, u2)

>>> Item.objects.all()
[<Item: 1:[<LiveTag: test>, <LiveTag: like>]>, <Item: 2:[<LiveTag: test>, <LiveTag: like>, <LiveTag: alpha>]>, <Item: 3:[<LiveTag: test>, <LiveTag: like>, <LiveTag: alpha>]>]
>>> g.search(Item.objects.filter(), ['like'])
[<Item: 1:[<LiveTag: test>, <LiveTag: like>]>, <Item: 2:[<LiveTag: test>, <LiveTag: like>, <LiveTag: alpha>]>, <Item: 3:[<LiveTag: test>, <LiveTag: like>, <LiveTag: alpha>]>]
>>> g.search(Item.objects.filter(), ['test'])
[<Item: 1:[<LiveTag: test>, <LiveTag: like>]>, <Item: 2:[<LiveTag: test>, <LiveTag: like>, <LiveTag: alpha>]>, <Item: 3:[<LiveTag: test>, <LiveTag: like>, <LiveTag: alpha>]>]
>>> g.search(Item.objects.filter(), ['alpha', 'test'])
[<Item: 2:[<LiveTag: test>, <LiveTag: like>, <LiveTag: alpha>]>, <Item: 3:[<LiveTag: test>, <LiveTag: like>, <LiveTag: alpha>]>]
>>> g.search(Item.objects.filter(), ['like', 'alpha', 'test'])
[<Item: 2:[<LiveTag: test>, <LiveTag: like>, <LiveTag: alpha>]>, <Item: 3:[<LiveTag: test>, <LiveTag: like>, <LiveTag: alpha>]>]
>>> g.search(Item.objects.filter(), ['like'], u1)
[<Item: 1:[<LiveTag: test>, <LiveTag: like>]>, <Item: 2:[<LiveTag: test>, <LiveTag: like>, <LiveTag: alpha>]>]
>>> g.search(Item.objects.filter(), ['like', 'alpha'], u1)
[<Item: 2:[<LiveTag: test>, <LiveTag: like>, <LiveTag: alpha>]>]
>>> g.search(Item.objects.filter(), ['like', 'alpha'], u2)
[<Item: 3:[<LiveTag: test>, <LiveTag: like>, <LiveTag: alpha>]>]
    """

class TextMinerTest(object):
    """
# init data
>>> u = User.objects.create(username='uuu1', password='uuu1')
>>> n = NounTag.objects.create(name="test", sub_type='T', user=u)
>>> n = NounTag.objects.create(name="English", sub_type='T', user=u)
>>> n = NounTag.objects.create(name=u'\u7d10\u7d04\u5e02', sub_type='T', user=u)
>>> n = NounTag.objects.create(name=u'\u707d\u96e3', sub_type='T', user=u)

# ASC-II test
>>> t = u'this is a simple test, and is for English only.'
>>> m = TextMiner()
>>> m.tags
frozenset([u'test', u'\u7d10\u7d04\u5e02', u'\u707d\u96e3', u'English'])
>>> m._tokenize(t)
[u'this', u'is', u'a', u'simple', u'test', u'and', u'is', u'for', u'English', u'only', u'']
>>> m.get_match_tags(t)
{u'test': 1, u'English': 1}

# Unicode test
>>> t = u'\u4e94\u628a\u9470\u5319\u5728\u624b\uff0c\u6703\u8b93\u7d10\u7d04\u5e02\u9677\u5165\u707d\u96e3\uff0c'
>>> m.get_match_tags(t)
{u'\u7d10\u7d04\u5e02': 1, u'\u707d\u96e3': 1}
    """