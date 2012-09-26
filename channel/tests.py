"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from channel.models import *

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_tag_duplicate_names(self):
        pass

u1 = User.objects.create_user(username='user1', password='us1')
u2 = User.objects.create_user(username='user2', password='us2')
u3 = User.objects.create_user(username='user3', password='us3')
u1.save()
u2.save()
u3.save()

p1 = Post(name='p1')
p1.save()
p2 = Post(name='p2')
p2.save()

nt = NounTag(name='nn1', type='T')
nt.save()

vt = VerbTag(name='vv1')
vt.save()

l = LiveTag(tag=nt, content_object=p1, tagger=u1)
l.save()
l = LiveTag(tag=vt, content_object=p2, tagger=u2)
l.save()