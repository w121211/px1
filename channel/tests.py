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

class InitTest(object):
    def init_data(self):
        # create function tags
        FunctionTag.objects.create(name='like')
        FunctionTag.objects.create(name='pin')

        # create noun tags
        NounTag.objects.create(name='test', sub_type='T')
        NounTag.objects.create(name='alpha', sub_type='T')

        # create verb tags
        VerbTag.objects.create(name='chat')
        VerbTag.objects.create(name='ask')
        VerbTag.objects.create(name='idea')