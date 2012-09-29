import functools

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseBadRequest
from django.utils.safestring import mark_safe
from django.utils.decorators import available_attrs
from django.utils import simplejson

from functools import wraps

_ERROR_MSG = '<!DOCTYPE html><html lang="en"><body><h1>%s</h1><p>%%s</p></body></html>'
_400_ERROR = _ERROR_MSG % '400 Bad Request'
_403_ERROR = _ERROR_MSG % '403 Forbidden'
_405_ERROR = _ERROR_MSG % '405 Not Allowed'

def ajax_view(func=None, method='GET', login_required=True, ajax_required=True):
    """
    Decorator for views that checks that the it is an ajax call, return an error
    if necessary.
    """
    def decorator(view_func):
        @functools.wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if request.method != method and method != 'REQUEST':
                return HttpResponseNotAllowed(mark_safe(_405_ERROR % ('Request must be a %s.' % method)))

            if ajax_required and not request.is_ajax():
                return HttpResponseForbidden(mark_safe(_403_ERROR % 'Request must be set via AJAX.'))

            if login_required and not request.user.is_authenticated():
                return HttpResponseForbidden(mark_safe(_403_ERROR % 'User must be authenticated!'))

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    if func:
        return decorator(func)
    return decorator