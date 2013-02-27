from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponse
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

def asset_view(request, asset_type=None):
    if asset_type:
        assets = Asset.objects.filter(asset_type__name__exact=asset_type).order_by('hostname')
    else:
        assets = Asset.objects.all().order_by('hostname')
    return view(request, 'asset_view', None, None, assets)

def asset_edit(request, asset_id):
    if request.method == "POST":
        asset = getAsset(asset_id)
        form = EditAsset(request.POST, instance=asset, asset_id=asset_id)
        if form.is_valid():
            form.save()
        else:
            return view(request, 'asset_edit', form.errors, asset_id)
    return view(request, 'asset_edit', None, asset_id)

def getInterface(iface_pk):
    print "Getting interface_by_id(%s)" % iface_pk
    return Interface.objects.get(pk=iface_pk)

def interface_edit(request, asset_id, interface_id):
    print "calling GET_INTERFACE."
    interface = getInterface(interface_id)
    if request.method == "POST":
        form = AddInterface(request.POST, instance=interface)
        try:
            form.is_valid()
        except:
            pass
        interface.name = form.cleaned_data['name']
        interface.ip4 = form.cleaned_data['ip4']
        interface.netmask = form.cleaned_data['netmask']
        interface.mac = form.cleaned_data['mac']
        interface.vlan = form.cleaned_data['vlan']
        interface.owner_id = asset_id
        partner = form.cleaned_data['partner']
        print "PARTNER=(%s)" % partner
        if partner is not None:
            interface_partner_id = partner
        elif partner == 0:
            interfaces.partner = None
        interface.save()
        return view(request, 'interface_edit', form.errors, interface.pk)
    else:
        return view(request, 'interface_edit', None, interface.pk)

@login_required
def view(request, route, form_errors=None, instance_id=None, assets=None):
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
    elif route == "asset_edit":
        asset = getAsset(instance_id)
        print "EditAsset(%s)" % asset.pk
        content_bag['form'] = EditAsset(instance=asset, asset_id=instance_id)
        content_bag['form_action'] = 'invdb.views.asset_edit'
        content_bag['asset_id'] = asset.pk
        content_bag['submit_txt'] = "Save Asset"
        content_bag['interface_form'] = AddInterface(owner=instance_id, interface_id=asset.primary_interface.id)
        content_bag['interfaces'] = getInterfaces(owner=asset.pk)
        viewname="asset_edit"
    elif route == "interface_edit":
        interface = getInterface(instance_id)
        print "EditInterface(%s)" % interface.pk
        content_bag['form'] = AddInterface(instance=interface, owner=interface.owner.id, interface_id=interface.pk)
        content_bag['asset_id'] = interface.owner.id
        content_bag['interface_id'] = interface.pk
        content_bag['submit_txt'] = "Save Interface"
        viewname="interface_edit"
    elif route == 'asset_view':
        viewname = "gridview"
        content_bag['assets'] = assets
    elif route == "home":
        viewname = 'home'
        content_bag['assets'] = Asset.objects.all().order_by('hostname')
        content_bag['assettypes'] = AssetType.objects.all().order_by('name')
        at_counts = {}
        for at in content_bag['assettypes']:
            cnt = Asset.objects.filter(asset_type=at).count()
            at_counts[at.name] = cnt
        content_bag['at_counts'] = at_counts
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
        'appname': "invdb",
    }
    return content_bag

def menutize(boo, pluralize=False, section='assets'):
    # boo: bunch of objects
    menu = []
    for o in boo:
        menuitem = {}
        menuitem['section'] = section
        menuitem['assettype'] = o.name

        if pluralize:
            menuitem['name'] = plural(o.name)
        else:
            menuitem['name'] = o.name

        menu.append(menuitem)
    return menu

def get_console(request, ahostname):
    try:
        asset = Asset.objects.get(hostname=ahostname)
    except:
        asset = None
    response = HttpResponse()
    if asset is not None:
        response.write("%s\n" % asset.console )
    else:
        response.write("None\n")
    return HttpResponse(response, mimetype="text/plain")

def getAssetTypes():
    assettypes = AssetType.objects.all().order_by('name')
    return assettypes

def getArea():
    areas = Area.objects.all().order_by('name')
    return areas

def interface_add(request, asset_id):
    if request.method == "POST":
        form = AddInterface(request.POST, owner=asset_id)
        asset = Asset.objects.get(pk=int(asset_id))
        try:
            form.is_valid()
        except:
            pass
        if asset:
            interface_name = form.cleaned_data['name']
            interface_ip4 = form.cleaned_data['ip4']
            interface_netmask = form.cleaned_data['netmask']
            interface_mac = form.cleaned_data['mac']
            interface_vlan = form.cleaned_data['vlan']
            interface_owner = asset
            partner = form.cleaned_data['partner']
            print "\n\TRYING TO PARTNER WITH %s" % partner
            interface = Interface.objects.get(pk=int(form.cleaned_data['partner'][0]))
            interface_partner = interface
            interface = Interface.create_full(interface_name,
                                         interface_ip4,
                                         interface_netmask,
                                         interface_mac,
                                         interface_vlan,
                                         interface_owner,
                                         interface_partner)
            interface.save()
            interface_partner.partner = interface
            interface_partner.save()
        else:
            return view(request, 'asset_edit', form.errors, asset_id)
    return view(request, 'asset_edit', None, asset_id)

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

def getAsset(asset_id=None):
    if asset_id is not None:
        print "searching for asset with pk=%s" % asset_id
        asset = Asset.objects.get(pk=asset_id)
        return asset
    else:
        assets = Asset.objects.all().order_by('hostname')
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
            asset_primary_interface_netmask = form.cleaned_data['primary_interface_netmask']
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

            interface = Interface.create(
                asset_primary_interface_name,
                asset_primary_interface_ip4,
                asset_primary_interface_netmask,
                asset_primary_interface_mac,
                asset_primary_interface_vlan,
                asset,

            )
            interface.save()
            asset.primary_interface = interface
            asset.save()
        else:
            return view(request, 'asset_add', form.errors)
    else:
        return view(request,'asset_add')
    return index(request)

