import sys

from django.core import serializers
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse

from account.decorators import login_required

from channel.models import Channel
from tagcanal.models import *
from tagcanal.utils import *
from stream.ajax import _response
from stream.decorators import ajax_view

def _get_channels(request):
    resp = {
        'alert': None,
        'channels': [],
        }
    qs = Channel.objects.filter(user=request.user)
    for channel in qs:
        resp['channels'].append(channel.to_json())
    return _response(resp)

@ajax_view
def get_channels(request):
    return _get_channels(request)

@ajax_view(method='POST')
def add_channel(request):
    Channel.objects.create(user=request.user)
    return _get_channels(request)

@ajax_view(method='POST')
def remove_channel(request):
    Channel.objects.get(id=request.POST['channel']).delete()
    return _get_channels(request)

@ajax_view(method='POST')
def add_tag(request):
    "add a tag to a channel"
    Channel.objects.get(id=request.POST['channel']).add_tag(request.POST['tag'])
    return _get_channels(request)

@ajax_view(method='POST')
def remove_tag(request):
    "remove a tag to a channel"
    Channel.objects.get(id=request.POST['channel']).remove_tag(request.POST['tag'])
    return _get_channels(request)