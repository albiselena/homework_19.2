from django import forms
from catalog.models import Product

from django import forms
from catalog.models import Product


class ProductForm(forms.ModelForm):
    forbidden_keywords = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                          'радар']

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        clean_data = self.cleaned_data['name'].lower()
        if any(keyword in clean_data for keyword in self.forbidden_keywords):
            raise forms.ValidationError('Это название содержит запрещенные слова.')
        return clean_data

    def clean_description(self):
        clean_data = self.cleaned_data['description'].lower()
        if any(keyword in clean_data for keyword in self.forbidden_keywords):
            raise forms.ValidationError('Описание содержит запрещенные слова.')
        return clean_data
