from bootstrap.forms import BootstrapForm, Fieldset
from django import forms

styles = {
    'textarea': {
        'rows': 7,
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

