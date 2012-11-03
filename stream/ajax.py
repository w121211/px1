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
from taggraph.utils import TagGraph
from taggraph.utils import TextMiner
from stream.models import *
from stream.decorators import ajax_view

POSTS_PER_PAGE = 5

_tagger = GeneralTagger()
_miner = TextMiner(NounTag.objects.all())

def _response(resp_data):
    resp = simplejson.dumps(resp_data, separators=(',', ':'))
    return HttpResponse(resp, mimetype='application/json')

def _paginate(queryset, item_num, time=None):
    """
    Return qs which <= time, with number of items specified
    """
    if len(time) == 0:
        return queryset.filter()[:item_num]
    else:
        return queryset.filter(created_time__lt=time)[:item_num]

@ajax_view
def get_posts(request):
    resp = {
        'alert': None,
        'posts': [],
        }
    tags = request.GET.get('t', None)
    time = request.GET.get('d', None)

    qs = Post.objects.all()
    if tags:
        # return posts by given tags
        tags = tags.split('+')
        qs = _tagger.search(qs, tags, request.user)
    else:
        # return my_stream posts
        qs = _paginate(qs, POSTS_PER_PAGE, time)

    for post in qs:
        resp['posts'].append(post.to_json(request.user))
    if len(resp['posts']) == 0:
        resp['alert'] = 'no matching posts'
    return _response(resp)

@ajax_view(method='POST')
def autotag_post(request):
    """
    Take a post content as input, find matching tags and return.
    {domain}/api/post/autotag/
    """
    resp = {
        'alert': None,
        'tags': [],
        }

    # Validate post content
    f = PostForm(request.POST)
    if not f.is_valid():
        resp['alert'] = "post title or body is not valid"
        return _response(resp)
    post = f.save(commit=False)

    # get matching tags
    g = TagGraph(_miner)
    g.add_text(post.title)
    g.add_text(post.body)
    #    resp['tags'] = list(g.direct_tags)
    resp['tags'] = g.get_recommend_tags()

    return _response(resp)

# TODO fix ajax redirect (302) error. (1) add ajaxRedirectResponse (2) using view div to display html
@ajax_view(method='POST')
def new_post(request):
    """
    Create a new post.
    {domain}/api/post/new/
    """
    resp = {
        'alert': None,
        }

    # Validate post content
    f = PostForm(request.POST)
    if not f.is_valid():
        resp['alert'] = "post title or body is not valid"
        return _response(resp)
    post = f.save(commit=False)
    post.user = request.user
    post.save()

    # add tags
    tags = request.POST.getlist('tags[]')
    _tagger.like.tag(post)
    _tagger.noun.bulk_tag(post, tags, request.user)

    return _response(resp)

@ajax_view(method='POST')
def reply_post(request):
    """
    Reply a post.
    {domain}/api/post/reply/
    """
    if (request.is_ajax()):
        if (request.method == 'POST'):
            data = simplejson.loads(request.body)
            p = Post()
            p.user = request.user
            p.reply_post_id = data['reply_post_id']
            p.thread = data['thread_id']
            p.title = data['title']
            p.body = data['body']
            p.save()
    return HttpResponse("OK")

@ajax_view(method='POST')
def push_post(request):
    """
    Create a push.
    {domain}/api/post/pu/
    """
    resp = {
        'alert': None,
        'pushes': [],
        }
    f = PushForm(request.POST)
    if not f.is_valid():
        resp['alert'] = f.errors.as_text()
        return _response(resp)
    push = f.save(commit=False)
    push.user = request.user
    push.save()

    _tagger.like.tag(push)
    resp['pushes'] = push.post.get_pushes(request.user)
    return _response(resp)

@ajax_view(method='POST')
def tag_post(request):
    """
    User tag a specified post.
    {domain}/api/tag/post/
    """
    resp = {
        'alert': None,
        'tags': [],
    }
    f = LivetagForm(request.POST)
    if not f.is_valid():
        resp['alert'] = f.errors
        return _response(f)
    try:
        p = Post.objects.get(id=f.cleaned_data['post'])
        _tagger.noun.tag(p, f.cleaned_data['tag'], request.user)
        resp['tags'] = p.get_tags(request.user)
    except ForbiddenTagError as e:
        resp['alert'] = "%s cannot be used as the tag" % e.tag
    return _response(resp)

@ajax_view
def vote_livetag(request):
    """
    User can vote a live tag (a tag of an object) with a given live tag id.
    {domain}/api/tag/vote/
    """
    resp = {
        'alert': None,
        'tags': [],
    }
    try:
        l = _tagger.vote(request.GET['t'], request.user)
        item = l.content_object
        resp['tags'] = item.get_tags(request.user)
    except LiveTag.DoesNotExist:
        resp['alert'] = "cannot find the live tag"
    return _response(resp)

def unvote_livetag(request):
    """
    User can vote a live tag (a tag of an object) with a given live tag id.
    {domain}/api/tag/unvote/
    """
    resp = {
        'alert': None,
        'tags': [],
        }
    try:
        l = _tagger.unvote(request.GET['t'], request.user)
        item = l.content_object
        resp['tags'] = item.get_tags(request.user)
    except LiveTag.DoesNotExist:
        resp['alert'] = "cannot find the live tag"
    return _response(resp)

def get_pushes(request):
    """
    Undecided function
    {domain}/json/push/get/
    """
    data = None
    if (request.is_ajax()):
        if (request.method == 'GET'):
            pushes = Push.objects.filter(post_id=request.GET['id'])
            if (pushes):
                data = list()
                for push in pushes:
                    data.append({
                        'user': push.user.__unicode__(),
                        'body': push.body,
                        })
                data = simplejson.dumps(data)
    if (data):
        return HttpResponse(data, mimetype='application/json')
    else:
        return HttpResponse('fail')