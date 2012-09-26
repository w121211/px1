from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Tag(models.Model):
    TYPES = (
        ('NN', 'Noun'),
        ('VB', 'Verb'),
        ('JJ', 'Adjective'),
        ('FN', 'Function'),
        )
    name = models.SlugField(max_length=50, unique=True)
    type = models.CharField(max_length=2, choices=TYPES)

    def __unicode__(self):
        return u"%s|%s" % (self.type, self.name)


class TermTag(Tag):
    class Meta:
        abstract = True


class NounTag(TermTag):
    SUB_TYPES = (
        ('H', 'Hub'),
        ('T', 'Terminal'),
        )
    type = models.CharField(max_length=2, default='NN', editable=False)
    sub_type = models.CharField(max_length=1, choices=SUB_TYPES)

    def __unicode__(self):
        return u"%s%s|%s" % (self.type, self.sub_type, self.name)


class VerbTag(TermTag):
    type = models.CharField(max_length=2, default='VB', editable=False)


class LiveTag(models.Model):
    tag = models.ForeignKey(Tag)
    tagger = models.ForeignKey(User, related_name='tagged_livetags')
    voters = models.ManyToManyField(User, related_name='voted_livetags')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def get_hits(self):
        return 0

    def is_hit(self, user):
        return False

    def __unicode__(self):
        return u"%s" % self.tag.name

    class Meta:
        unique_together = ('content_type', 'object_id', 'tag')


class Push(models.Model):
    name = models.CharField(max_length=10)


class Post(models.Model):
    name = models.CharField(max_length=10)
    tags = generic.GenericRelation(LiveTag)

    def __unicode__(self):
        return u"%s" % self.name