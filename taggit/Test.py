from taggit.models import *
from forum.models import Post

p = Post.objects.filter(title='1')

ItemBase.tag_model()

class D(object):
    def a(self):
        pass

class C(object):
    def __init__(self):
        self.name = 'C'
    def __get__(self, instance, owner):
        print(instance)
        print(owner)
        return self.name
    def set_name(self, name):
        self.name = name
    def print_name(self):
        print(self.name)

class T(object):
    c = C()

    def __init__(self):
        self.inst_attr = 'inst_attr'
    def m1(self):

        print 'm1', self.attr, self.inst_attr

