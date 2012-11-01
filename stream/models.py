from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.db import models
from django.forms import ModelForm

from tagcanal.models import NounTag
from tagcanal.models import LiveTag

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


class Thread(models.Model):
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%d-%s" % (self.id, self.title)

    @models.permalink
    def get_absolute_url(self):
        return 'stream.views.view_thread', [str(self.id)]


class Post(TaggableItem):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    repost = models.ForeignKey('self', null=True, blank=True)
#    thread = models.ForeignKey(Thread)
    title = models.CharField(max_length=40)
    body = models.TextField()

    def __unicode__(self):
        return u"%s" % (self.id)

    def get_pushes(self, user):
        l = list()
        for p in self.push_set.all():
            l.append(p.to_json(user))
        return l

    def to_json(self, user):
        post = {
            'id': self.id,
#            'tid': self.thread_id,
            'reid': self.repost_id,
            'user': self.user.username,
            'time': self.time.strftime('%Y-%m-%dT%H:%M:%S'),
            'title': self.title,
            'body': self.body,
            'tags': self.get_tags(user),
            'pushes': self.get_pushes(user)
        }
        return post

    @models.permalink
    def get_absolute_url(self):
        return 'stream.views.view_post', [str(self.id)]


class Push(TaggableItem):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    body = models.CharField(max_length=140)

    def __unicode__(self):
        return u"%s @%s" % (self.body, self.user)

    def to_json(self, user):
        p = {
            'user': self.user.username,
            'body': self.body,
            'tags': self.get_tags(user),
        }
        return p

class Channel(models.Model):
    user = models.ForeignKey(User)
    tags = models.ManyToManyField(NounTag)

    def to_json(self):
        j = {
            'tags': self.tags
        }
        return j


class ThreadForm(ModelForm):
    class Meta:
        model = Thread


class PostForm(ModelForm):
    class Meta:
        model = Post
#        include = ('title', 'body')
        exclude = ('user')


class PushForm(ModelForm):
    class Meta:
        model = Push
