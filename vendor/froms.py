from django import forms
from .models import vendor
from accounts.validators import allow_only_image_validator


class VendorForm(forms.ModelForm):
    vendor_licence = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}),
                                     validators=[allow_only_image_validator])

    class Meta:
        model = vendor
        fields = ['vendor_name', 'vendor_licence']
