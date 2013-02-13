from bootstrap.forms import BootstrapForm, Fieldset
from django import forms
from invdb.models import *

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

class AddAsset(BootstrapForm):
    class Meta:
        layout = (
            Fieldset("Add Asset", "asset_type", "hostname", "alt_id", "model", "serial", "purchase_date",
                     "eth0_ip", "eth0_mac", "eth0_partner", "console", "notes",
                     "physical_status", "logical_status", "rack"),
        )
    asset_type = forms.ModelChoiceField(queryset=AssetType.objects.all(), empty_label=None)
    alt_id = forms.CharField(max_length=50, widget=forms.TextInput(attrs=styles['textbox']), initial="Managed Services Reference ID")
    model = forms.CharField(max_length=50, widget=forms.TextInput(attrs=styles['textbox']), initial="SKU0 - Dell R410 96GB + 16TB RAID6")
    serial = forms.CharField(max_length=50, widget=forms.TextInput(attrs=styles['textbox']))
    purchase_date = forms.DateField(widget=forms.TextInput(attrs=styles['textbox']), required=False)
    provision_date = forms.DateField(widget=forms.TextInput(attrs=styles['textbox']), required=False)
    decommission_date = forms.DateField(widget=forms.TextInput(attrs=styles['textbox']), required=False)
    hostname = forms.CharField(max_length=50, widget=forms.TextInput(attrs=styles['textbox']))
    eth0_ip = forms.IPAddressField(widget=forms.TextInput(attrs=styles['textbox']), required=False)
    eth0_mac = forms.CharField(max_length=12, widget=forms.TextInput(attrs=styles['textbox']), required=False)
    eth0_partner = forms.ModelChoiceField(queryset=Asset.objects.all(), required=False)
    console = forms.CharField(max_length=50, widget=forms.TextInput(attrs=styles['textbox']), required=False)
    notes = forms.CharField(max_length=255, widget=forms.TextInput(attrs=styles['textbox']), required=False)
    physical_status = forms.ModelChoiceField(queryset=PhysicalStatusCode.objects.all(), empty_label=None)
    logical_status = forms.ModelChoiceField(queryset=LogicalStatusCode.objects.all(), empty_label=None)
    rack = forms.ModelChoiceField(queryset=Rack.objects.all(), required=False)
#        rack_u = forms.ModelChoiceField()
#        rack_u_size = forms.ModelChoiceField()
