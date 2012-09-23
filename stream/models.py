from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

class Thread(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=40)

    def __unicode__(self):
        return u"%d-%s" % (self.id, self.title)

    @models.permalink
    def get_absolute_url(self):
        return 'stream.views.view_thread', [str(self.id)]

class Post(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    reply_post = models.ForeignKey('self', null=True, blank=True)
    thread = models.ForeignKey(Thread)
    title = models.CharField(max_length=40)
    body = models.TextField(max_length=10000)
#    tags = TaggableManager()

    def __unicode__(self):
        return u"%s @%s" % (self.id, self.user)

    def to_json(self):
        post = {
            'id': self.id,
            'thread_id': self.thread_id,
            'user': self.user.username,
            'time': self.created_time.isoformat(' '),
            'title': self.title,
            'body': self.body
        }
        return post

    @models.permalink
    def get_absolute_url(self):
        return ('stream.views.view_post', [str(self.id)])

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

class ThreadForm(ModelForm):
    class Meta:
        model = Thread

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('user','reply_post', 'thread')

class PushForm(ModelForm):
    class Meta:
        model = Push
