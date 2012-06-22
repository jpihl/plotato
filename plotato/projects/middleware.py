from django.utils.encoding import iri_to_uri
from django.http import HttpResponse
from django.template import RequestContext
from django.conf import settings
from django.contrib import messages

def is_authorized(request):
    return request.session.has_key('is_authorized') and request.session['is_authorized'] == settings.ADMIN_PASSWORD

class HttpResponseReload(HttpResponse):
    status_code = 302
    def __init__(self, request):
        HttpResponse.__init__(self)
        http_referer = request.META.get('HTTP_REFERER')
        self['Location'] = iri_to_uri(http_referer or "/")

def admin_only(function=None):
    """Check that the admin is logged in.

    This decorator ensures that the view functions it is called on can be 
    accessed only by the admin. When an non-admin accesses
    such a protected view, they are redirected to the address specified in 
    the field named in `next_field` or, lacking such a value, the home view
    """
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            if not is_authorized(request):
                messages.add_message(request, messages.ERROR, 'ERROR: Unauthorized, please login.')
                return HttpResponseReload(request)
            else:
                return view_func(request, *args, **kwargs)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)