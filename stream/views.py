from django.core import serializers
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse

from account.decorators import login_required

from stream.models import *

@login_required
def index(request):
    """
    Show an index page

    {domain}/{forum_url}/
    """
    threads = Thread.objects.all()
    return render_to_response('stream/index.html', {'threads': threads})

@login_required
def view_post(request, post_id):
    """
    Show a single post and all pushes reply to this post.

    {domain}/{stream}/post/{post_id}/
    """
    post = Post.objects.get(id=post_id)
    pushes = post.push_set.all()
    return render_to_response('stream/post.html', {
        'post': post, 'pushes': pushes})

@login_required
def get_post_html(request, post):
    """
    Internal use only. Return a html context contains a single post and all pushes reply to this post.

    """
    pushes = post.push_set.all()
    return render_to_string('stream/post.html', {
        'post': post, 'pushes': pushes})

@login_required
def view_thread(request, thread_id):
    """
    Show a single post and all pushes reply to this post.

    {domain}/{stream}/post/{thread_id}/
    """
    thread = Thread.objects.get(id=thread_id)
    posts = thread.post_set.all()
    post_htmls = list()
    for post in posts:
        post_htmls.append(get_post_html(request, post))
    return render_to_response('stream/thread.html', {'post_htmls': post_htmls})

@login_required # TODO fix ajax redirect (302) error. (1) add ajaxRedirectResponse (2) using view div to display html
def post(request):
    """
    AJAX action. Submit a new post.

    {domain}/{stream}/json/post/
    """
    print('post view')
    if (request.is_ajax()):
        if (request.method == 'POST'):
            data = simplejson.loads(request.body)
            title = data['title']
            body = data['body']
            if (len(title) < 1 or len(body) < 10):
                return HttpResponse("fail")
            t = Thread()
            t.title = title
            t.save()
            print t

            p = Post()
            p.user = request.user
            p.thread = t
            p.title = title
            p.body = body
            p.save()
            print p
    return HttpResponse("ok")

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
def push(request):
    """
    AJAX action.

    {domain}/{stream}/json/push/
    """
    if (request.is_ajax()):
        if (request.method == 'POST'):
            json = simplejson.loads(request.body)
            p = Push()
            p.user = request.user
            p.post_id = json['post_id']
            p.body = json['push_body']
            p.save()
#            print json
    return HttpResponse("OK")

def get_pushes(request):
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