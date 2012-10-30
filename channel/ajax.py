import sys

from django.core import serializers
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse

from account.decorators import login_required

from tagcanal.models import *
from tagcanal.utils import *
from stream.models import *
from stream.decorators import ajax_view

@ajax_view
def get_channels(request):
    resp = {
        'alert': None,
        'chas': [],
        }
    tags = request.GET.get('t', None)
    date = request.GET.get('d', None)

    qs = Post.objects.filter(user=request.user)
    if len(tags) == 0: # return my_stream posts
        qs = _paginate(qs, POSTS_PER_PAGE, date)
    else: # return posts by given tags
        tags = str(tags).split('+')
        qs = _tagger.search(qs, tags, request.user)

    for post in qs:
        resp['posts'].append(post.to_json(request.user))
    if len(resp['posts']) == 0:
        resp['alert'] = 'error: can not find any posts'
    return _response(resp)

def new_channel(request):
    pass

def tag_channel(request):
    "add a tag from a tagcanal"
    pass

def untag_channel(request):
    "remove a tag from a tagcanal"
    pass