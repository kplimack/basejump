from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from bootstrap.forms import BootstrapForm, Fieldset
from invdb.models import *
import datetime

styles = {
    'textarea': {
        'rows': 4,
        'class': "field span9",
        'style': "resize:none;"
    },
    'textbox': {
        'class': "input-large span9",
    },
}

class AddArea(BootstrapForm):
    class Meta:
        layout = (
            Fieldset("Add Area", "name", "address", "phone", "email","website", "notes" ),
        )
    name = forms.CharField(max_length=50,required=True,widget=forms.TextInput(attrs=styles['textbox']))
    address = forms.CharField(max_length=200,widget=forms.Textarea(attrs=styles['textarea']))
    phone = forms.CharField(max_length=16,widget=forms.TextInput(attrs=styles['textbox']))
    email = forms.CharField(max_length=50,widget=forms.TextInput(attrs=styles['textbox']), initial="noc@colo.com")
    website = forms.CharField(max_length=255,widget=forms.TextInput(attrs=styles['textbox']), initial="tickets.colo.com")
    notes = forms.CharField(required=False,widget=forms.Textarea(attrs=styles['textarea']))

class AddRack(BootstrapForm):
    class Meta:
        layout = (
            Fieldset("Add Rack", "name", "area", "numu"),
        )
    name = forms.CharField(max_length=20, widget=forms.TextInput(attrs=styles['textbox']))
    area = forms.ModelChoiceField(queryset=Area.objects.all())
    numu = forms.IntegerField()

def getInterfaces(asset_type_name=None, *args, **kwargs ):
    result_list = []
    owner_id = kwargs.pop('owner', '')
    if owner_id:
        interfaces = Interface.objects.filter(owner__exact=owner_id)
        return interfaces or None
    if asset_type_name is not None:
        print "Searching for interfaces of type %s" % asset_type_name
        assettype = AssetType.objects.get(name__exact=asset_type_name)
        if assettype:
            print "found %s" % assettype.name
        else:
            print "SEARCH FOR ASSETTYPE FAILED"
            return None
        print "searching for Interfaces of AssetType %s" % assettype.name
        ifaces = Interface.objects.filter(partner__isnull=True, owner__asset_type__exact=assettype)
        if ifaces:
            print "Found %s ifaces" % ifaces.count()
        else:
            print "Search for Interfaces had 0 results"
            return None
    else:
        print "Searching for interfaces that are not parnered"
        ifaces = Interface.objects.filter(partner__isnull=True)
    if not ifaces.count():
        print "NO LONLY INTERFACES FOUND"
        return None
    for iface in ifaces:
        result_list.append(iface)
    print "\n\ngetInterfaces: %s\n\n" % result_list
    return result_list

class EditAsset(forms.ModelForm):
    class Meta:
        model=Asset
    def __init__(self, *args, **kwargs):
        asset_id = kwargs.pop('asset_id', '')
        super(EditAsset, self).__init__(*args, **kwargs)
  #      available_pdu_ports = getInterfaces('PDU')
 #       if available_pdu_ports is not None:
 #           self.fields['pdu0_id'] = forms.ChoiceField(choices = [ (pdu.pk, pdu.owner.hostname + " - " + pdu.name) for pdu in available_pdu_ports])
 #       else:
 #           self.fields['pdu0_id'] = forms.ChoiceField(choices = [ (0, '---')])
        asset = Asset.objects.get(pk=asset_id)
        print "\n\nFINDING PRIMARY INTERFACE FOR %s" % asset.hostname
        self.fields['primary_interface'] = forms.ModelChoiceField(queryset=Interface.objects.filter(pk__exact=asset.primary_interface.id))
#        self.fields['pdu0_id'].required=False
#        self.fields['pdu0_id'].initial = 0

class AddInterface(forms.ModelForm):
    class Meta:
        model=Interface

    def __init__(self, *args, **kwargs):
        owner_id = kwargs.pop('owner', '')
        interface_id = kwargs.pop('interface_id', '')
        super(AddInterface, self).__init__(*args, **kwargs)
        if owner_id:
            owner = Asset.objects.get(pk=int(owner_id))
        self.fields['owner'] = forms.CharField()
        self.fields['owner'].widget.attrs['readonly'] = True
        try:
            self.fields['owner'].initial = owner
        except:
            pass
        self.fields['partner'] = forms.ChoiceField(choices = [ (iface.id, iface.owner.hostname + " - " + iface.name) for iface in getInterfaces()], initial=0)
        self.fields['partner'].required=False
        self.fields['partner'].choices.append((0, "---"))
        if interface_id:
            interface = Interface.objects.get(pk=interface_id)
            print "\n\nINTERFACE_PARTNER=(%s)" % interface.partner
            if interface.partner is not None:
                self.fields['partner'].initial = interface.partner
            else:
                print "SETTING INITIAL TO 0"
                self.fields['partner'].initial=0

class AddAsset(BootstrapForm):
    class Meta:
        layout = (
            Fieldset("Add Asset",
                     "asset_type",
                     "hostname",
                     "alt_id",
                     "model",
                     "serial",
                     "console",
                     "purchase_date",
                     "provision_date",
                     "primary_interface_name",
                     "primary_interface_ip4",
                     "primary_interface_netmask",
                     "primary_interface_mac",
                     "primary_interface_vlan",
                     "primary_interface_partner",
                     "physical_status",
                     "logical_status",
                     "rack",
                     "notes",),
        )
    def __init__(self, *args, **kwargs):
        super(AddAsset, self).__init__(*args, **kwargs)
        interfaces = getInterfaces()
        if interfaces is not None:
            self.fields['primary_interface_partner'] = forms.ChoiceField(choices = [ (iface.id, iface.owner.hostname + " - " + iface.name) for iface in getInterfaces()], initial=0)
        else:
            self.fields['primary_interface_partner'] = forms.ChoiceField()
        self.fields['primary_interface_partner'].required=False
        self.fields['primary_interface_partner'].choices.append((0, "---"))

    now = datetime.datetime.now()
    asset_type = forms.ModelChoiceField(queryset=AssetType.objects.all(), empty_label=None)
    alt_id = forms.CharField(max_length=50, widget=forms.TextInput(attrs=styles['textbox']), initial="Managed Services Reference ID")
    model = forms.CharField(max_length=50, widget=forms.TextInput(attrs=styles['textbox']), initial="SKU0 - Dell R410 96GB + 16TB RAID6")
    serial = forms.CharField(max_length=50, widget=forms.TextInput(attrs=styles['textbox']))
    purchase_date = forms.DateField(widget=forms.TextInput(attrs=styles['textbox']), required=False)
    provision_date = forms.DateField(widget=forms.TextInput(attrs=styles['textbox']), required=False, initial=datetime.date.today())  #now.strftime("%Y-%m-%d"))
    decomission_date = forms.DateField(widget=forms.TextInput(attrs=styles['textbox']), required=False)
    hostname = forms.CharField(max_length=50, widget=forms.TextInput(attrs=styles['textbox']))
    primary_interface_name = forms.CharField(max_length=10, widget=forms.TextInput(attrs=styles['textbox']), initial="eth0")
    primary_interface_ip4 = forms.IPAddressField(widget=forms.TextInput(attrs=styles['textbox']), required=False)
    primary_interface_netmask = forms.IPAddressField(widget=forms.TextInput(attrs=styles['textbox']), required=False)
    primary_interface_mac = forms.CharField(max_length=12, widget=forms.TextInput(attrs=styles['textbox']), required=False)
    primary_interface_vlan = forms.CharField(widget=forms.TextInput(attrs=styles['textbox']), initial="0")
    console = forms.CharField(max_length=50, widget=forms.TextInput(attrs=styles['textbox']), required=False)
    notes = forms.CharField(max_length=255, widget=forms.Textarea(attrs=styles['textarea']), required=False)
    physical_status = forms.ModelChoiceField(queryset=PhysicalStatusCode.objects.all(), empty_label=None)
    logical_status = forms.ModelChoiceField(queryset=LogicalStatusCode.objects.all(), empty_label=None)
    rack = forms.ModelChoiceField(queryset=Rack.objects.all(), required=False, empty_label="Disabled")
#        rack_u = forms.ModelChoiceField()
#        rack_u_size = forms.ModelChoiceField()

