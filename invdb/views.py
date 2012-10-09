from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import *
from django.contrib.auth import login, authenticate, logout

def index(request):
    if not request.user.is_authenticated():
        return render_to_response('login.html',
                                  context_instance=RequestContext(request))
    else:
        user = request.user
        return render_to_response('index.html',
                                  context_instance=RequestContext(request))
