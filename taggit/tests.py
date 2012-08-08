from django.db import models
from django.utils import unittest
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from taggit.managers import TaggableManager


class Seed(models.Model):
    tags = TaggableManager()


class TagTestCase(unittest.TestCase):
    def setUp(self):
        self.seed = Seed.objects.create()

    def test_tags_add(self):
        self.seed.tags.add('t1', 't2', 't3')
        self.assertEqual(self.seed.tags.all(), ['t1', 't2', 't3'])

    def test_tags_remove(self):
        pass

    def test_tags_find_models(self):
        pass

