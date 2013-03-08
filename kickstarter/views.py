from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.template import RequestContext
from django.contrib.auth.models import *
from django import template
from basejump.plural import plural
from basejump.urlizer import urlize
from basejump.ipmi import *
from kickstarter.models import *
from kickstarter.forms import *
from invdb.models import Asset
from basejump.checker import *
import ipaddr
import re

def index(request):
    if not request.user.is_authenticated():
        return view(request, 'login')
    else:
        return view(request, 'home')

def view(request, route, form_errors=None, instance_id=None, assets=None):
    content_bag = getCommonContent()
    print "route = %s" % route
    if route == 'server_view':
        content_bag['servers'] = Asset.objects.filter(asset_type__name__exact='Server')
        content_bag['bootoptions'] = getBootOptions()
        viewname = "kickstart_servers"
    elif route == 'settings_view':
        settings = kssettings.objects.all()
        service_checks = ServiceCheck.objects.all()
        checkResults = runChecks(service_checks)
        content_bag['service_checks'] = service_checks
        content_bag['checkResults'] = checkResults
        content_bag['form'] = EditSetting()
        content_bag['settings'] = settings
        viewname = 'kickstart_settings'
    elif route == 'settings_edit':
        content_bag['form'] = EditSetting()
        content_bag['form_action'] = 'kickstarter.views.settings_view'
        viewname = "formview"
    elif route == "bootoptions_view":
        content_bag['bootoptions'] = getBootOptions()
        content_bag['form'] = AddBootOption()
        viewname = 'kickstart_bootoptions'
    elif route == "bootoptions_add":
        content_bag['form'] = AddBootOption()
    elif route == 'bootoptions_edit':
        content_bag['form'] = AddBootOption()
    else:
        viewname = 'kickstart'
    print "rendering viewname(%s)" % viewname
    print "\n\nCONTENT_BAG:\n%s\n\n" % content_bag
    return render_to_response(viewname + '.html', content_bag, context_instance=RequestContext(request))


def getCommonContent():
    content_bag = {}
    content_bag['appname'] = "kickstarter"
    content_bag['kssettings'] = kssettings.objects.all()
    return content_bag

def getBootOptions():
    boot_options = BootOption.objects.all()
    return boot_options

def server_view(request):
    return view(request, 'server_view')

def settings_view(request):
    return view(request, 'settings_view')

def bootoptions_view(request):
    return view(request, 'bootoptions_view')

def bootoptions_edit(request):
    return view(request, 'bootoptions_edit')

def bootoptions_add(request):
    if request.method == "POST":
        form = AddBootOption(request.POST)
        if form.is_valid():
            form.save()
            return view(request, 'bootoptions_view')
        else:
            return view(request, 'bootoptions_add', form.errors)
    return view(request, 'bootoptions_add')

def settings_add(request):
    if request.method == "POST":
        form = EditSetting(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            new_setting = form.cleaned_data['setting']
            new_setting = kssettings.create(name, new_setting)
            new_setting.save()
            return settings_view(request)

def getSetting(setting_key):
    settings = kssettings.objects.get(name__exact=setting_key)
    return settings.setting

def get_ksconfig(request, hostname, opsys, release, arch):
    asset = Asset.objects.get(hostname=hostname)
    print "Getting ksconfig for %s" % asset.hostname
    return kickme(request, opsys, release, arch, asset)

def kickme(request, opsys, release, arch, asset=None):
    masks = {
        '255.255.255.255': 32,
        '255.255.255.252': 30,
        '255.255.255.248': 29,
        '255.255.255.240': 28,
        '255.255.255.224': 27,
        '255.255.255.192': 26,
        '255.255.255.128': 25,
        '255.255.255.0': 24,
        '255.255.254.0': 23,
        '255.255.252.0': 22,
        '255.255.248.0': 21,
        '255.255.240.0': 20,
        '255.255.224.0': 19,
        '255.255.192.0': 18,
        '255.255.128.0': 17,
        '255.255.0.0': 16,
        '255.254.0.0': 15,
        '255.252.0.0': 14,
        '255.248.0.0': 13,
        '255.240.0.0': 12,
        '255.224.0.0': 11,
        '255.192.0.0': 10,
        '255.128.0.0': 9,
        '255.0.0.0': 8,
        '254.0.0.0': 7,
        '252.0.0.0': 6,
        '248.0.0.0': 5,
        '240.0.0.0': 4,
    }

    response = HttpResponse(content_type="text/plain")
    debugging =  "Operating System: %s\nRelease: %s\nArch: %s\n" % (opsys, release, arch)
    log = open('kicker.log', 'w')
    log.write("%s" % request)
    if asset is None:
        CLIENT_MAC = None
        try:
            # The interface names are not consistant with mac_<index>, you'll have to check each
            # 'HTTP_X_RHN_PROVISIONING_MAC_0': 'em1 90:B1:1C:28:CA:F1',
            # 'HTTP_X_RHN_PROVISIONING_MAC_1': 'p1p4 A0:36:9F:11:E4:A3',
            # 'HTTP_X_RHN_PROVISIONING_MAC_2': 'em2 90:B1:1C:28:CA:F2',
            # 'HTTP_X_RHN_PROVISIONING_MAC_3': 'p1p3 A0:36:9F:11:E4:A2',
            # 'HTTP_X_RHN_PROVISIONING_MAC_4': 'p1p1 A0:36:9F:11:E4:A0',
            # 'HTTP_X_RHN_PROVISIONING_MAC_5': 'p1p2 A0:36:9F:11:E4:A1',
            #ifname = asset.primary_interface.name
            #print "SEARCHING FOR MACADDR OF %s" % ifname
            ifname = "em1"
            for i in range(0, 5):
                cur_mac = request.META['HTTP_X_RHN_PROVISIONING_MAC_' + str(i)]
                print "CHECKING for %s" % cur_mac
                if ifname in str(cur_mac):
                    CLIENT_MAC = str(cur_mac)
        except KeyError:
            response.write("NO MAC ADDRES SENT IN REQUEST\n")
            return response
        if CLIENT_MAC is None:
            msg = "MAC ADDR NOT FOUND IN REQUEST"
            response.write(msg)
            print "%s" % msg
            return msg
        CLIENT_MAC = CLIENT_MAC.partition(' ')[2].replace(':','')
        try:
            asset = Asset.objects.get(primary_interface__mac=CLIENT_MAC)
        except:
            response.write("Could not find asset with MAC: '%s'\n" % CLIENT_MAC)
            return response
    else:
        CLIENT_MAC = asset.primary_interface.mac
    CLIENT_IP = asset.primary_interface.ip4
    if CLIENT_IP is None:
        response.write("NO CLIENT IP IN DATABASE\n")
        return response
    if asset.hostname is None:
        response.write("CLIENT_HOSTNAME NOT DEFINED FOR INTEFFACE WITH MAC: %s\n" % CLIENT_MAC)
        return response
    CLIENT_NETMASK=asset.primary_interface.netmask
    print "ASSET INFO: %s/%s(%s)/%s" % (CLIENT_IP, CLIENT_NETMASK, masks[CLIENT_NETMASK], CLIENT_MAC)
    addr = ipaddr.IPNetwork(str(CLIENT_IP) + "/" + str(masks[CLIENT_NETMASK]))
    CLIENT_GATEWAY = addr.network + 1
    CLIENT_NS=getSetting('PXE_NS1')
    ksconfig = open('kickstarter/ksconfigs/ksconfig', 'r').read()
    ksconfig = ksconfig.replace('__NETWORK__', '--bootproto=static --ip=' + str(CLIENT_IP) + ' --netmask=' + str(CLIENT_NETMASK) + ' --gateway=' + str(CLIENT_GATEWAY) + ' --nameserver=' + str(CLIENT_NS) + ' --hostname ' + str(asset.hostname))
    REPO = getSetting('REPO_URL')
    REPO = REPO.replace('__OS__', opsys)
    REPO = REPO.replace('__RELEASE__', release)
    REPO = REPO.replace('__ARCH__', arch)
    ksconfig = ksconfig.replace('__REPO_URL__', REPO)
    ksconfig = ksconfig.replace('__BASEJUMP_URL__', request.META['HTTP_HOST'])
    ksconfig = ksconfig.replace('__ARCH__', arch)
    ksconfig = ksconfig.replace('__ASSET_ID__', str(asset.id))
    log.write("Returning the following ksconfig:\n%s" % ksconfig)
    response.write(ksconfig)
    #else:
    #    response.write("IP ADDRESS FOR (%s) NOT FOUND IN INVENTORY:\n" % CLIENT_MAC)
    return response

def get_repo(request, reponame):
    if ".repo" in reponame:
        filename = "repos/" + reponame
        return returnFile(request, filename)
    else:
        response = HttpResponse(content_type="text/plain")
        msg = "Not a valid repo\n"
        print "%s" % msg
        response.write(msg)
        return response

def returnFile(request, filename):
    import os.path
    import mimetypes
    mimetypes.init()
    try:
        file_path = settings.PROJECT_DIR + '/kickstarter/' + filename
        print "FILEPATH TO SERVE: %s" % file_path
        fsock = open(file_path,"r")
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        mime_type_guess = mimetypes.guess_type(file_name)
        if mime_type_guess is not None:
            response = HttpResponse(fsock, mimetype=mime_type_guess[0])
            response['Content-Disposition'] = 'attachment; filename=' + file_name
        else:
            response = HttpResponse(content_type="text/plain")
            response.write(fsock)
    except:
        response = HttpResponseNotFound()
    return response

def chef_validator(request):
    return returnFile(request, "chef-validation.pem")

def chef_client(request):
    return returnFile(request, "chef-client.rb")


def BootFileName(mac):
    tftp_root = getSetting('TFTP_ROOT')
    pxe_root = tftp_root + '/pxelinux.cfg'
    mac_pxe_file = pxe_root + '/01-' + re.sub("(.{2})", "\\1-", mac, re.DOTALL)[:17]
    return mac_pxe_file

def checkBootOption(asset_id):
    default_boot = "localboot"
    asset = Asset.objects.get(pk=asset_id)
    if asset is not None:
        mac = asset.primary_interface.mac
        if mac is None:
            return default_boot
        mac_pxe_file = BootFileName(mac)
        print "CHECKING TFTP_ROOT FOR PXE FILE: (%s)" % mac_pxe_file
        pxe_boot_option = readLink(mac_pxe_file)
        print "%s --> %s" % (mac_pxe_file, pxe_boot_option)
            # read the link (00-aa-bb-cc-dd-ee -> /data/tftpboot/pxelinux.cfg/centos6.3)
            #               (00-aa-bb-cc-dd-ef -> /data/tftpboot/pxelinux.cfg/localboot)
    return default_boot

def bootoptions_get_assetid(request, asset_id):
    bootoption = checkBootOption(asset_id)
    print "THE BOOTOPTION FOR (%s) is (%s)" % (asset_id, bootoption)
    return returnJSON(bootoption)

def bootoptions_get_macaddr(request, macaddr):
    # normalize the mac to HEX, no dashes, uppercase
    mac = str(macaddr.replace("-", ""))
    mac = mac.upper()
    asset = Asset.objects.get(primary_interface__mac=mac)
    return bootoptions_get_assetid(request, asset.pk)

# I think that using jQuery to mess with the form is screwing up CSRF validation
# which results in a HTTP/403 Response, but no futher explanation
@csrf_exempt
def servers_kick(request):
    # this function needs to do 2 parts
    # 1. create the BootOption file
    # 2. reboot the server
    print "GOT REBOOT REQUEST"
    if request.method == "POST":
        asset_id = request.POST['asset_id']
        bootoption_id = request.POST['select_pxe_option']
        asset = Asset.objects.get(pk=asset_id)
        mac = asset.primary_interface.mac
        mac_file = BootFileName(mac)
        print "SETTING BOOTOPTION TO %s" % bootoption_id
        if linkExists(mac_file):
            print "REMOVING OLD SYMLINK %s" % mac_file
            os.unlink(mac_file)
        if bootoption_id == "localboot":
            print "CREATING SYMLINK (%s -> localbootl)" % mac_file
            os.symlink("localboot", mac_file)
        else:
            bootoption = BootOption.objects.get(pk=bootoption_id)
            print "CREATING SYMLINK (%s -> %s)" % (mac_file, bootoption.label)
            os.symlink(bootoption.label, mac_file)
        print "SENDING POWER CYCLE SIGNAL VIA IPMI"
        powerCycle(asset.console)
        return HttpResponse("GOOD:\n%s" % request.POST, mimetype="text/plain")
    else:
        return HttpResponse(status=204)

def servers_release(request, asset_id):
    response = HttpResponse(content_type="text/plain")
    try:
        asset=Asset.objects.get(pk=asset_id)
    except:
        msg = "ASSET(%s) NOT FOUND TO RELEASE" % asset_id
        print "%s" % msg
        response.write("%s\n" % msg)
        return response
    mac = asset.primary_interface.mac
    mac_file = BootFileName(mac)
    if fileExists(mac_file):
        msg = "REMOVING MAC_FILE(%s)" % mac_file
        response.write("%s\n" % msg)
        print "%s" % msg
        os.remove(mac_file)
    else:
        msg = "FileNotFound MAC_FILE(%s)" % mac_file
        response.write("%s\n" % msg)
        print "%s" % msg
    return response

def returnJSON(to_json):
    return HttpResponse(simplejson.dumps(to_json), mimetype="application/json")
