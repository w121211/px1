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
        ('FB', 'Forbidden'),
        )
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    name = models.SlugField(max_length=50, unique=True)
    type = models.CharField(max_length=2, choices=TYPES)

    def __unicode__(self):
        return u"%s|%s" % (self.type, self.name)


class ForbiddenTag(Tag):
    def __init__(self, *args, **kwargs):
        super(ForbiddenTag, self).__init__(*args, **kwargs)
        self.type = 'FB'


class FunctionTag(Tag):
    def __init__(self, *args, **kwargs):
        super(FunctionTag, self).__init__(*args, **kwargs)
        self.type = 'FN'


class WordTag(Tag):
    class Meta:
        abstract = True


class NounTag(WordTag):
    SUB_TYPES = (
        ('H', 'Hub'),
        ('T', 'Terminal'),
        )
    sub_type = models.CharField(max_length=1, choices=SUB_TYPES, default='T')

    def __init__(self, *args, **kwargs):
        super(NounTag, self).__init__(*args, **kwargs)
        self.type = 'NN'

    def __unicode__(self):
        return u"%s%s|%s" % (self.type, self.sub_type, self.name)


class VerbTag(WordTag):
    def __init__(self, *args, **kwargs):
        super(VerbTag, self).__init__(*args, **kwargs)
        self.type = 'VB'

### Tagger ###

class LiveTag(models.Model):
    tag = models.ForeignKey(Tag)
    user = models.ForeignKey(User, related_name='tagged_livetags')
    voters = models.ManyToManyField(User, related_name='voted_livetags')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return u"%s" % self.tag.name

    def vote(self, user):
        self.voters.add(user)

    def unvote(self, user):
        self.voters.remove(user)

    def get_votes(self):
        return self.voters.count()

    def is_vote(self, user):
        q = self.voters.filter(id=user.id)
        if q.count() > 0:
            return True
        else:
            return False

    def to_json(self, user):
        j = {
            'id': self.id,
            'type': self.tag.type,
            'name': self.tag.name,
            'myvote': self.is_vote(user),
            'votes': self.get_votes(),
        }
        return j

    class Meta:
        unique_together = ('content_type', 'object_id', 'tag')


class Item(models.Model):
    user = models.ForeignKey(User)
    tags = generic.GenericRelation(LiveTag, related_name="%(app_label)s_%(class)s_tags")

    def __unicode__(self):
        return u"%d:%s" % (self.id, self.tags.all())


class TaggableItem(models.Model):
    tags = generic.GenericRelation(LiveTag, related_name="%(app_label)s_%(class)s_tags")

    def get_tags(self, user):
        l = list()
        for t in self.tags.select_related(depth=5).all():
            l.append(t.to_json(user))
        return l

    class Meta:
        abstract = True
        ordering = ('-time',)