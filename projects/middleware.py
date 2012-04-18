from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, get_object_or_404

class PermissionDeniedToLoginMiddleware(object):
    def process_exception(self, request, exception):
    	print "HELLO FROM PermissionDeniedToLoginMiddleware"
        if type(exception) == PermissionDenied:
            messages.add_message(request, messages.ERROR, 'ERROR: Access denied, please login in as authorized user!')
            return HttpResponseRedirect('/')
        return None

def get_manageable_object_or_404(cls, user, *args, **kwds):
    item = get_object_or_404(cls, *args, **kwds)
    if not item.user_can_manage_me(user):
        raise PermissionDenied()
    return item