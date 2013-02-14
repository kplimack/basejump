from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import *
from basejump.plural import plural
from basejump.urlizer import urlize
from invdb.models import *
from invdb.forms import *

def index(request):
    if not request.user.is_authenticated():
        return view(request, 'login')
    else:
        return view(request, 'home')


def view(request, route, form_errors=None):
    content_bag = get_common_content(request)
    content_bag['form_errors'] = form_errors
    if content_bag['areas'].count() < 1:
        route="area_add"
    if route == "area_add":
        content_bag['form'] = AddArea(initial=request.POST)
        content_bag['form_action'] = 'invdb.views.area_add'
        content_bag['submit_txt'] = "Add Area"
        viewname = "formview"
    elif route == "asset_add":
        content_bag['form'] = AddAsset(initial=request.POST)
        content_bag['form_action'] = 'invdb.views.asset_add'
        content_bag['submit_txt'] = "Add Asset"
        viewname = "formview"
    else:
        viewname = route
    print "VIEWNAME=%s" % viewname
    print "\n\nCONTENT BAG\n%s\n\n" % content_bag
    return render_to_response(viewname + '.html', content_bag, context_instance=RequestContext(request))

def get_common_content(request):
    areas = getArea()
    content_bag = {
        'nav_left_menu': menutize(getAssetTypes(), True, "assets"),
        'user': request.user,
        'areas': areas,
        'areas_menu': menutize(areas, False, "areas"),
    }
    return content_bag

def menutize(boo, pluralize=False, urlpath=None):
    # boo: bunch of objects
    menu = []
    for o in boo:
        menuitem = {}
        if urlpath:
            menuitem['url'] = urlize(urlpath + '/' + o.name)
        else:
            menuitem['url'] = '#'

        if pluralize:
            menuitem['name'] = plural(o.name)
        else:
            menuitem['name'] = o.name

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
            return view(request, 'area_add', form.errors)
    else:
        return view(request,'area_add')
    return index(request)

def getAsset():
    assets = Asset.objects.all().order_by('name')
    return assets

def asset_add(request):
    if request.method == "POST":
        form = AddAsset(request.POST)
        if form.is_valid():
            asset_type = form.cleaned_data['asset_type']
            asset_model = form.cleaned_data['model']
            asset_serial = form.cleaned_data['serial']
            asset_purchase_date = form.cleaned_data['purchase_date']
            asset_hostname = form.cleaned_data['hostname']
            asset_alt_id = form.cleaned_data['alt_id']
            asset_primary_interface_name = form.cleaned_data['primary_interface_name']
            asset_primary_interface_ip4 = form.cleaned_data['primary_interface_ip4']
            asset_primary_interface_mac = form.cleaned_data['primary_interface_mac']
            asset_primary_interface_vlan = form.cleaned_data['primary_interface_vlan']
            asset_primary_interface_partner = form.cleaned_data['primary_interface_partner']
            asset_console = form.cleaned_data['console']
            asset_notes = form.cleaned_data['notes']
            asset_physical_status = form.cleaned_data['physical_status']
            asset_logical_status = form.cleaned_data['logical_status']
            asset_rack = form.cleaned_data['rack']
            asset_rack_u = 1 #form.cleaned_data['rack_u']
            asset_rack_u_size = 1 #form.cleaned_data['rack_u_size']
            asset = Asset.create(
                asset_model,
                asset_type,
                asset_serial,
                asset_purchase_date,
                asset_hostname,
                asset_primary_interface_name,
                asset_primary_interface_ip4,
                asset_primary_interface_mac,
                asset_primary_interface_vlan,
                asset_primary_interface_partner,
                asset_console,
                asset_notes,
                asset_physical_status,
                asset_logical_status,
                asset_rack,
                asset_rack_u,
                asset_rack_u_size,
                asset_alt_id
            )
            asset.save()
        else:
            return view(request, 'asset_add', form.errors)
    else:
        return view(request,'asset_add')
    return index(request)

