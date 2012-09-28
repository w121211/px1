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

_tagger = GeneralTagger()

@login_required
def get_post_html(request, post):
    """
    Internal use only. Return a html context contains a single post and all pushes reply to this post.

    """
    pushes = post.push_set.all()
    return render_to_string('stream/post.html', {
        'post': post, 'pushes': pushes})

def _paginate(queryset, item_num, time=None):
    """
    Return qs which <= time, with number of items specified
    """
    if len(time) == 0:
        return queryset.filter()[:item_num]
    else:
        return queryset.filter(created_time__lt=time)[:item_num]

@login_required
def api_get_posts(request):
    POSTS_PER_PAGE = 2
    data = {
        'msg': None,
        'posts': [],
        }
    if request.is_ajax() and request.method == 'GET':
        tags = request.GET.get('t', None)
        date = request.GET.get('d', None)

        qs = Post.objects.all()
        if len(tags) == 0:
            # return my_stream posts
            qs = _paginate(qs, 5, date)
        else:
            # return posts by given tags
            tags = str(tags).split('+')
            qs = _tagger.search(qs, tags, request.user)

        if qs.count() != 0:
            data['msg'] = 'ok'
            for post in qs:
                data['posts'].append(post.to_json(request.user))
        else:
            data['msg'] = 'no posts'
        data = simplejson.dumps(data, separators=(',', ':'))
    return HttpResponse(data, mimetype='application/json')

@login_required
def _api_get_posts(request):
    """
    Return posts(json) by an ajax call.

    {domain}//api/post/get/
    """
    POSTS_PER_PAGE = 2
    data = {
        'msg': None,
        'posts': [],
        }
    if request.is_ajax() and request.method == 'GET':
        try:
            if 't' in request.GET:
            # return channel posts
            #                tags = str(request.GET['t']).split('+')
                t = request.GET
                tag_names = str(t).split('+')
                print "return posts by given tags"
                print t
            else:
                # return my_stream posts
                last_post_id = int(request.GET['lp'])
                print "last pd: %d" % last_post_id
                if (last_post_id <= 0):
                    posts = Post.objects.all()
                else:
                    posts = Post.objects.filter(id__lt=last_post_id)
                posts = posts.order_by('-created_time')[:POSTS_PER_PAGE]

                if posts:
                    for post in posts:
                        data['posts'].append(post.to_json(request.user))
                    data['msg'] = 'ok'
                else:
                    data['msg'] = 'no posts'
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
    return HttpResponse(simplejson.dumps(data, separators=(',', ':')), mimetype='application/json')

# TODO fix ajax redirect (302) error. (1) add ajaxRedirectResponse (2) using view div to display html
@login_required
def api_new_post(request):
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
def api_reply_post(request):
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
def api_push_post(request):
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

def api_get_pushes(request):
    """
    AJAX action.

    {domain}/{stream}/json/push/get/
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

def api_add_tag(request):
    """
    An ajax action, user can add a tag to a specified post.

    {domain}/api/tag/add/
    """
    pass

def api_vote_live_tag(request):
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
