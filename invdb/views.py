from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import *
from basejump.plural import plural
from invdb.models import *
from invdb.forms import *

def index(request):
    if not request.user.is_authenticated():
        return view(request, 'login')
    else:
        return view(request, 'home')


def view(request, viewname):
    content_bag = get_common_content(request)
    if viewname == "area_add":
        content_bag['form'] = AddArea()
        content_bag['form_action'] = 'invdb.views.area_add'
        content_bag['submit_txt'] = "Add Form"
    print "\n\nCONTENT BAG\n%s\n\n" % content_bag
    return render_to_response(viewname + '.html', content_bag, context_instance=RequestContext(request))

def get_common_content(request):
    areas = getArea()
    if not areas:
        return view(request, "area_add")
    content_bag = {
        'nav_left_menu': menutize(getAssetTypes()),
        'user': request.user,
        'areas': areas,
    }
    return content_bag

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
    assettypes = AssetType.objects.all().order_by('name')
    return assettypes

def getArea():
    areas = Area.objects.all().order_by('name')
    return areas

def area_add(request):
    if request.method == "POST":
        form = AddArea(request.POST)
        if form.is_valid():
            area_name = form.cleaned_data['name']
            area_address = form.cleaned_data['address']
            area_phone = form.cleaned_data['phone']
            area_email = form.cleaned_data['email']
            area_website = form.cleaned_data['website']
            area_notes = form.cleaned_data['notes']
            area = Area.create(area_name, area_phone, area_address, area_email, area_website, area_notes)
            area.save()
    else:
        return view(request,'area_add')
    return index(request)
