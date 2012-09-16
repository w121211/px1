from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from account.decorators import login_required
from taggit.models import Tag

from px1.settings import MEDIA_ROOT, MEDIA_URL
from forum.models import *

#class ProfileForm(ModelForm):
#    class Meta:
#        model = UserProfile
#        exclude = ["posts", "user"]

def add_csrf(request, **kwargs):
    """Add CSRF to dictionary."""
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d

def mk_paginator(request, items, num_items):
    "Create and return a paginator."
    paginator = Paginator(items, num_items)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items

def index(request):
    """Listing of available boards.
    {forum_url}/
    """
    boards = Board.objects.all()
    return render_to_response("forum/index.html", add_csrf(request, boards=boards))

def tag(request):
    """Listing of all tags.
    {forum_url}/tag/
    """
    tags = Tag.objects.all()
    return render_to_response('forum/tag.html', {'tags': tags})

def tag_board(request):
    """Listing of posts in a board depends on given tags.
    {forum_url}/tag/board/
    """
    tags = request.GET.getlist('t')
    posts = Post.objects.filter(tags__name__in=tags).distinct()
    posts = mk_paginator(request, posts, 20)
    return render_to_response('forum/tag_board.html',
                              add_csrf(request, posts=posts))

def board(request, board_id):
    """Listing of posts in a board.
    {forum_url}/board/{board_id}/
    """
    posts = Post.objects.filter(board=board_id).order_by('-created')
    posts = mk_paginator(request, posts, 20)
    return render_to_response("forum/board.html",
                              add_csrf(request, posts=posts, board_id=board_id))

def new_board(request):
    """Creating a new board
    {forum_url}/board/new/
    """
    b = request.POST
    if b['title']:
        Board.objects.create(title=b['title'])
    return HttpResponseRedirect(reverse('forum.views.index'))

def thread(request, thread_id):
    """Listing of posts in a thread.
    {forum_url}/board/thread/{thread_id}/
    """
    t = Thread.objects.get(id=thread_id)
    posts = Post.objects.filter(thread=t).order_by("created")
    posts = mk_paginator(request, posts, 15)
    #t = Thread.objects.get(pk=pk)
    return render_to_response("forum/thread.html",
        add_csrf(request, posts=posts, pk=thread_id, title=t.title, media_url=MEDIA_URL))

#@login_required
#def profile(request, pk):
#    """Edit user profile."""
#    profile = UserProfile.objects.get(user=pk)
#    img = None
#
#    if request.method == "POST":
#        pf = ProfileForm(request.POST, request.FILES, instance=profile)
#        if pf.is_valid():
#            pf.save()
#            # resize and save image under same filename
#            imfn = pjoin(MEDIA_ROOT, profile.avatar.name)
#            im = PImage.open(imfn)
#            im.thumbnail((160,160), PImage.ANTIALIAS)
#            im.save(imfn, "JPEG")
#    else:
#        pf = ProfileForm(instance=profile)
#
#    if profile.avatar:
#        img = "/media/" + profile.avatar.name
#    return render_to_response("forum/profile.html", add_csrf(request, pf=pf, img=img))


def view_post(request, post_id):
    """Display a post.
    {forum_url}/post/{post_id}/
    """
    post = Post.objects.get(id=post_id)


@login_required
def post(request, post_type, post_id):
    """Display a post form.
    {forum_url}/post/new_thread/{post_id}
    {forum_url}/post/reply/{post_id}
    """
    action = reverse("forum.views.%s" % post_type, args=[post_id])
    if post_type == "new_thread":
        title = "Start New Topic"
        subject = ''
    elif post_type == "reply":
        title = "Reply"
        subject = "Re: " + Post.objects.get(id=post_id).thread.title
    pf = PostForm()
    return render_to_response("forum/post.html", add_csrf(
        request, subject=subject, action=action, title=title, post_form=pf))

#def increment_post_counter(request):
#    profile = request.user.userprofile_set.all()[0]
#    profile.posts += 1
#    profile.save()

@login_required
def new_thread(request, board_id):
    """Start a new thread.
    {forum_url}/new_thread/{board_id}
    """
    f = PostForm(request.POST)
    if f.is_valid():
        p = f.save(commit=False)
        p.board = Board.objects.get(id=board_id)
        p.thread = Thread.objects.create(title=p.title, creator=request.user)
        p.creator = request.user
        p.save()
        f.save_m2m()
    return HttpResponseRedirect(reverse('forum.views.board', args=[board_id]))

@login_required
def reply(request, post_id):
    """Reply to a thread.
    {forum_url}/reply/{post_id}
    """
    f = PostForm(request.POST)
    if f.is_valid():
        p = f.save(commit=False)
        p.board = Post.objects.get(id=post_id).board
        p.thread = Post.objects.get(id=post_id).thread
        p.creator = request.user
        p.save()
        f.save_m2m()
    return HttpResponseRedirect(reverse('forum.views.board', args=[board_id]))