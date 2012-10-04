import sys

from django.core import serializers
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse

from account.decorators import login_required

from channel.models import *
from channel.utils import *
from stream.models import *
from stream.decorators import ajax_view

POSTS_PER_PAGE = 5

_tagger = GeneralTagger()

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
        'msg': None,
        'posts': [],
        }
    tags = request.GET.get('t', None)
    date = request.GET.get('d', None)

    qs = Post.objects.all()
    if len(tags) == 0: # return my_stream posts
        qs = _paginate(qs, POSTS_PER_PAGE, date)
    else: # return posts by given tags
        tags = str(tags).split('+')
        qs = _tagger.search(qs, tags, request.user)

    for post in qs:
        resp['posts'].append(post.to_json(request.user))
    if len(resp['posts']) > 0:
        resp['msg'] = 'ok'
    else:
        resp['msg'] = 'no posts'
    return _response(resp)

# TODO fix ajax redirect (302) error. (1) add ajaxRedirectResponse (2) using view div to display html
@login_required
def new_post(request):
    """
    an ajax action. Submit a new post.

    {domain}/api/post/new/
    """
    resp_data = {
        'msg': None,
        }
    if request.is_ajax() and request.method == 'POST':
        try:
        # saving a thread
        #            f = ThreadForm(request.POST)
        #            thread = f.save()

            # saving a post
            print request.POST
            f = PostForm(request.POST)
            post = f.save(commit=False)
            post.user = request.user
            #            post.thread = thread
            post.save()

            # add tags
            _tagger.like.tag(post)

        except:
            print "Error:", sys.exc_info()[0]
    return HttpResponse()

@login_required
def reply_post(request):
    """
    AJAX action. Reply a post.

    {domain}/{stream}/json/post/reply/
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

@login_required
def push_post(request):
    """
    AJAX action.

    {domain}/{stream}/json/push/
    """
    if request.is_ajax():
        if request.method == 'POST':
            json = simplejson.loads(request.body)
            p = Push()
            p.user = request.user
            p.post_id = json['post_id']
            p.body = json['push_body']
            p.save()
        #            print json
    return HttpResponse("OK")

ajax_view
def tag_post(request):
    """
    User tag a specified post.
    {domain}/api/tag/post/
    """
    resp = {
        'msg': '',
        'tag': '',
    }
    p = request.GET.get('id', None)
    t = request.GET.get('t', None)
    if p or t:
        resp['msg'] = 'error: empty tag or post'
    else:
        _tagger.noun.tag(p, t, request.user)
        resp['tag'] = t
    return _response(resp)

def get_pushes(request):
    """
    AJAX action.
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

def vote_live_tag(request):
    """
    An ajax action, user can vote a live tag (a tag of an object) with a given live tag id.

    {domain}/api/tag/vote/
    """
    resp = {
        'votes': None
    }
    if request.is_ajax() and 'i' in request.GET:
        t = LiveTag.objects.get(id=request.GET['i'])
        t.vote(request.user)
        resp['votes'] = t.get_votes()
    return HttpResponse(simplejson.dumps(resp, separators=(',', ':')),
        mimetype='application/json')

def get_channels(request):
    pass

def new_channel(request):
    pass

def tag_channel(request):
    "add a tag from a channel"
    pass

def untag_channel(request):
    "remove a tag from a channel"
    pass