from django.contrib import admin

from stream.models import *

admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(Push)