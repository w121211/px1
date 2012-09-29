from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.db import models
from django.forms import ModelForm

from channel.models import LiveTag

class Thread(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=40)

    def __unicode__(self):
        return u"%d-%s" % (self.id, self.title)

    @models.permalink
    def get_absolute_url(self):
        return 'stream.views.view_thread', [str(self.id)]

    class Meta:
        ordering = ('-created_time',)

class Post(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    reply_post = models.ForeignKey('self', null=True, blank=True)
#    thread = models.ForeignKey(Thread)
    title = models.CharField(max_length=40)
    body = models.TextField(max_length=10000)
    tags = generic.GenericRelation(LiveTag)

    def __unicode__(self):
        return u"%s @%s" % (self.id, self.user)

    def get_tags(self, user):
        l = list()
        for t in self.tags.select_related(depth=5).all():
            l.append(t.to_json(user))
        return l

    def to_json(self, user):
        post = {
            'id': self.id,
#            'thread_id': self.thread_id,
            'user': self.user.username,
            'time': self.created_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'title': self.title,
            'body': self.body,
            'tags': self.get_tags(user),
        }
        return post

    @models.permalink
    def get_absolute_url(self):
        return ('stream.views.view_post', [str(self.id)])

    class Meta:
        ordering = ('-created_time',)

#    def short(self):
#        return u"%s - %s\n%s" % (self.creator, self.title, self.created.strftime("%b %d, %I:%M %p"))
#    short.allow_tags = True

class Push(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    body = models.CharField(max_length=140)

    def __unicode__(self):
        return u"%s @%s" % (self.body, self.user)

    class Meta:
        ordering = ('-created_time',)

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
