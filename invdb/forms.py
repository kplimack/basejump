from bootstrap.forms import BootstrapForm, Fieldset
from django import forms

class AddArea(BootstrapForm):
    class Meta:
        layout = (
            Fieldset("Add Area", "name", "address", "phone", "email","website", "notes" ),
        )
    name = forms.CharField(max_length=50,required=True)
    address = forms.CharField(max_length=200,widget=forms.Textarea)
    phone = forms.CharField(max_length=16)
    email = forms.CharField(max_length=50)
    website = forms.CharField(max_length=255)
    notes = forms.CharField(widget=forms.Textarea)
