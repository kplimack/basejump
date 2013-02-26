import gspread
from invdb.models import Asset, Interface, AssetType, PhysicalStatusCode, LogicalStatusCode
from django.http import Http404, HttpResponseRedirect, HttpResponse
import datetime

doc_name = 'Carpathia Buildsheet'
sheet_name = "Build Info"
sheet_num = 4
email = "kyle.plimack@gmail.com"
password = "exwlsusqonzckiwm" # one-time password for 2-step auth

gc = gspread.login(email, password)
wks = gc.open(doc_name).get_worksheet(sheet_num)

# whoever decided to take form over function here really made this harder than it had to be
first_row = 16
last_row = 533 # not the last row, but the last one that we'll iterate not including idiot buffers
blocksize = 11

schema = {
    'order_num': 2,
    'hostname': 4,
    'model': 5,
    'ram': 6,
    'cpu': 7,
    'serial': 12,
    'alt_id': 13,
    'eth0_ip': 22,
    'eth0_netmask': 24,
    'eth0_vlan': 19,
    'eth0_mac': 26,
    'console': 22,
}

idiot = {
    'order_num': 0,
    'hostname': 5,
    'model': 0,
    'ram': 0,
    'cpu': 0,
    'serial': 0,
    'alt_id': 0,
    'eth0_mac': 0,
    'eth0_ip': 0,
    'eth0_netmask': 0,
    'eth0_vlan': 0,
    'console': 10
}

incomplete_hosts = []
SERVER = AssetType.objects.get(pk=1)
PHYS_UNKNOWN = PhysicalStatusCode.objects.get(pk=1)
LOGI_UNKNOWN = LogicalStatusCode.objects.get(pk=1)

def index(request):
    response = HttpResponse(content_type="text/plain")

    for row in range(first_row, last_row, blocksize):
        current_host = wks.cell(row + idiot['hostname'], schema['hostname'])
        n = {}
        for f in schema:
        #    print "LOOKING UP COORDS (%s, %s)" % (row + idiot[f], schema[f])
            v = wks.cell(row + idiot[f], schema[f]).value
            if v is None:
                if f in ["serial", "alt_id", "eth0_mac", "console"]:
                    incomplete_hosts.append("Missing %s from %s" % (f, current_host))
                v = None
            if v is not None:
                v = v.replace("\n", " ")
            print "%s: %s" % (f, v)
            response.write("%s: %s\n" % (f, v))
            n[f] = v
        asset = Asset.create(
            n['model'] + " " + n['ram'] + " " + n['cpu'],
            SERVER,
            n['serial'],
            str(datetime.datetime.now().strftime("%Y-%m-%d")),
            n['hostname'],
            n['console'],
            "",
            PHYS_UNKNOWN,
            LOGI_UNKNOWN,
            None, # Rack
            None, # Rack U
            None, # Rack U Size
            n['alt_id'])
        response.write("SAVING ASSET:\n\n")
        asset.save()
        interface = Interface.create(
            "eth0", # primary interface name
            n['eth0_ip'],
            n['eth0_netmask'],
            n['eth0_mac'],
            n['eth0_vlan'],
            asset
        )
        response.write("CREATING INTERFACE:\n\n")
        interface.save()
        asset.primary_interface = interface
        response.write("UPDATING ASSET's INTERFACE\n")
        response.write("===================================================\n")
        asset.save()

        print "==========================================================="

    print "Errors:\n"
    response.write("\nERRORS:\n")
    for e in incomplete_hosts:
        print " * %s" % e
        response.write(" * %s\n" % e)
    print
    return response
