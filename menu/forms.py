from django import forms

from accounts.validators import allow_only_image_validator
from menu.models import Category, FoodItem
from django.core.exceptions import ValidationError


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']

    def __init__(self, *args, **kwargs):
        self.vendor = kwargs.pop('vendor', None)
        super().__init__(*args, **kwargs)

    def clean_category_name(self):
        category_name = self.cleaned_data.get('category_name')
        if Category.objects.filter(category_name=category_name, vendor=self.vendor).exists():
            raise ValidationError('Category with this name already exists for this vendor.')
        return category_name


class FoodItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}),
                            validators=[allow_only_image_validator])

    class Meta:
        model = FoodItem
        fields = ['category', 'food_title', 'description', 'price', 'image', 'is_available']

    def __init__(self, *args, **kwargs):
        vendor = kwargs.pop('vendor', None)
        super(FoodItemForm, self).__init__(*args, **kwargs)
        if vendor:
            self.fields['category'].queryset = Category.objects.filter(vendor=vendor)
