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
    email = forms.CharField(max_length=50,widget=forms.TextInput(attrs=styles['textbox']))
    website = forms.CharField(max_length=255,widget=forms.TextInput(attrs=styles['textbox']))
    notes = forms.CharField(widget=forms.Textarea(attrs=styles['textarea']))

class AddRack(BootstrapForm):
    class Meta:
        layout = (
            Fieldset("Add Rack", "name", "area", "numu"),
        )
    name = forms.CharField(max_length=20, widget=forms.TextInput(attrs=styles['textbox']))
    area = forms.ModelChoiceField(queryset=Area.objects.all())
    numu = forms.IntegerField()

class AddDevice(BootstrapForm):
    class Meta:
        layout = (
            Fieldset("Add Asset", "type", "model", "serial", "purchase_date", "hostname",
                     "eth0_ip", "eth0_mac", "eth1_ip", "eth1_mac", "console", "notes",
                     "physical_status", "logical_status", "rack", "rack_u", "rack_u_size"),
        )
        model = forms.CharField(max_length=50, widget=forms.TextInput(attrs=styles['textbox']))
        serial = forms.CharField(max_length=50, widget=forms.TextInput(attrs=styles['textbox']))
        purchase_date = forms.DateField(widget=forms.TextInput(attrs=styles['textbox']))
        hostname = forms.CharField(max_length=50, widget=forms.TextInput(attrs=styles['textbox']))
        eth0_ip = forms.IPAddressField(widget=forms.TextInput(attrs=styles['textbox']))
        eth0_mac = forms.CharField(max_length=12, widget=forms.TextInput(attrs=styles['textbox']))
        eth1_ip = forms.IPAddressField(widget=forms.TextInput(attrs=styles['textbox']))
        eth1_mac = forms.CharField(max_length=12, widget=forms.TextInput(attrs=styles['textbox']))
        console = forms.CharField(max_length=50, widget=forms.TextInput(attrs=styles['textbox']))
        notes = forms.CharField(max_length=255, widget=forms.TextInput(attrs=styles['textbox']))
        physical_status = forms.ModelChoiceField(queryset=PhysicalStatusCode.objects.all())
        logical_status = forms.ModelChoiceField(queryset=LogicalStatusCode.objects.all())
        rack = forms.ModelChoiceField(queryset=Rack.objects.all())
#        rack_u = forms.ModelChoiceField()
#        rack_u_size = forms.ModelChoiceField()
