from bootstrap.forms import BootstrapForm, Fieldset
from django import forms

class AddArea(BootstrapForm):
    class Meta:
        layout = (
            Fieldset("Add Area", "name", "address", "phone", "email", ),
        )
    name = forms.CharField(max_length=50)
    address = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=16)
    email = forms.CharField(max_length=50)
