from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import *
from django.contrib.auth import login, authenticate, logout
from invdb.models import *
from basejump.plural import plural

def index(request):
    if not request.user.is_authenticated():
        return render_to_response('login.html',
                                  context_instance=RequestContext(request))
    else:
        user = request.user
        content_bag = {
            'nav_left_menu': menutize(getAssetTypes()),
            }
        print "\n\nCONTENT BAG\n%s\n\n" % content_bag
        return render_to_response('index.html', content_bag,
                                  context_instance=RequestContext(request))


def menutize(boo):
    # boo: bunch of objects
    menu = []
    for o in boo:
        menuitem = {
            'name': plural(o.name),
            'url': '#',
            }
        menu.append(menuitem)
    return menu

def getAssetTypes():
    results = AssetType.objects.all().order_by('name')
    return results
