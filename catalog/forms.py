from django import forms
from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('user',)
        fields = ('name', 'description', 'photo', 'creation_date', 'price', 'category', 'is_published')

    def clean_name(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        cleaned_data = self.cleaned_data['name']
        for word in forbidden_words:
            if word.lower() in cleaned_data:
                raise forms.ValidationError('Запрещенное слово')
        return cleaned_data

    def clean_description(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        cleaned_data = self.cleaned_data['description']
        for word in forbidden_words:
            if word.lower() in cleaned_data:
                raise forms.ValidationError('Запрещенное слово')
        return cleaned_data


class ProductModerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('is_published', 'description', 'category',)


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
