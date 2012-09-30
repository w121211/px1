from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.db import models
from django.forms import ModelForm

from channel.models import LiveTag

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
    created_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=40)

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
    body = models.TextField(max_length=10000)

    def __unicode__(self):
        return u"%s" % (self.id)

    def get_posts(self):
        l = list()
        for p in self.push_set.all():
            l.append(p.to_json())
        return l

    def to_json(self, user):
        post = {
            'id': self.id,
#            'thread_id': self.thread_id,
            'user': self.user.username,
            'time': self.time.strftime('%Y-%m-%dT%H:%M:%S'),
            'reid': self.repost_id,
            'title': self.title,
            'body': self.body,
            'tags': self.get_tags(user),
        }
        return post

    @models.permalink
    def get_absolute_url(self):
        return ('stream.views.view_post', [str(self.id)])


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
