from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from bootstrap.forms import BootstrapForm, Fieldset
from kickstarter.models import *
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

class EditSetting(forms.ModelForm):
    class Meta:
        model=kssettings
    def __init__(self, *args, **kwargs):
        super(EditSetting, self).__init__(*args, **kwargs)
        self.fields['permanent'].widget = forms.HiddenInput()

class AddBootOption(forms.ModelForm):
    class Meta:
        model=BootOption
    def __init__(self, *args, **kwargs):
        super(AddBootOption, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs=styles['textbox'])
        self.fields['label'].widget = forms.TextInput(attrs=styles['textbox'])
        self.fields['kernel'].widget = forms.TextInput(attrs=styles['textbox'])
        self.fields['append'].widget = forms.TextInput(attrs=styles['textbox'])

# class EditAsset(forms.ModelForm):
#     class Meta:
#         model=Asset
#     def __init__(self, *args, **kwargs):
#         asset_id = kwargs.pop('asset_id', '')
#         super(EditAsset, self).__init__(*args, **kwargs)
#         asset = Asset.objects.get(pk=asset_id)
#         print "\n\nFINDING PRIMARY INTERFACE FOR %s" % asset.hostname
#         self.fields['primary_interface'] = forms.ModelChoiceField(queryset=Interface.objects.filter(pk__exact=asset.primary_interface.id))

# class AddInterface(forms.ModelForm):
#     class Meta:
#         model=Interface

#     def __init__(self, *args, **kwargs):
#         owner_id = kwargs.pop('owner', '')
#         super(AddInterface, self).__init__(*args, **kwargs)
#         if owner_id:
#             owner = Asset.objects.get(pk=int(owner_id))
#         self.fields['owner'] = forms.CharField()
#         self.fields['owner'].widget.attrs['readonly'] = True
#         self.fields['owner'].initial = owner
#         self.fields['partner'] = forms.ChoiceField(choices = [ (iface.id, iface.owner.hostname + " - " + iface.name) for iface in getInterfaces()], initial=0)
#         self.fields['partner'].required=False
#         self.fields['partner'].choices.append((0, "---"))
