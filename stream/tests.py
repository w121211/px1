"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from channel.models import *
from channel.tests import InitTest as ChannelInitTest
from stream.models import *


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class InitTest(object):
    def init_data(self):
        try:
            # require channel.tests.InitTest.init_data() to run first
            i = ChannelInitTest()
            i.init_data()
        except:
            print "data is exist"

        # create test users
        auto = User.objects.create_user(username='auto', password='auto')
        u1 = User.objects.create_user(username='uuu1', password='uuu1')
        u2 = User.objects.create_user(username='uuu2', password='uuu2')
        u3 = User.objects.create_user(username='uuu3', password='uuu3')

        # create posts
        p1 = Post.objects.create(user=u1)
        p2 = Post.objects.create(user=u2)

        # create live tags
        t1 = Tag.objects.get(name='like')
        t2 = Tag.objects.get(name='pin')
        t3 = Tag.objects.get(name='test')
        LiveTag.objects.create(content_object=p1, tag=t1, tagger=auto)
        LiveTag.objects.create(content_object=p1, tag=t2, tagger=auto)
        LiveTag.objects.create(content_object=p1, tag=t3, tagger=u1)
        LiveTag.objects.create(content_object=p2, tag=t1, tagger=auto)
        LiveTag.objects.create(content_object=p2, tag=t2, tagger=auto)
        LiveTag.objects.create(content_object=p2, tag=t3, tagger=u2)