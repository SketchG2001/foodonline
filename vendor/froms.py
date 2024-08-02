from django import forms
from .models import vendor


class VendorForm(forms.ModelForm):
    class Meta:
        model = vendor
        fields = ['vendor_name', 'vendor_licence']
