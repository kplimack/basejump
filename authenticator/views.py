from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import *
from django.contrib.auth import login, authenticate, logout
from invdb.views import *
from authenticator.forms import *

def index(request):
    print "ADFD"
    if not request.user.is_authenticated():

        return render_to_response('login.html', {
            'form': LoginForm(),
    },                                  context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('invdb.views.index'))

def login_user(request):
    msg = "Please login below..."
    username = password = ''
    success = False
    print "FAVCE"
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                success=True
            else:
                msg = "Account not found"
        else:
            msg = "Incorrect username/password"
        if success:
            return HttpResponseRedirect(reverse('invdb.views.index'))
        else:
            return render_to_response('login.html', {
                'error': msg,
                'username': username,
                'form': LoginForm(),
            }, context_instance=RequestContext(request))
    else:
        print "DURKLA"
        return render_to_response('login.html', {
            'form': LoginForm(),
        }, context_instance=RequestContext(request))

def logout_user(request):
    logout(request)
    return index(request)
