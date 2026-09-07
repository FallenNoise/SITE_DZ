from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # Добавьте другие поля модели, если нужно (например, 'description')
        fields = ['name', 'price', 'description']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and len(name) < 6:
            raise forms.ValidationError(
                "Название товара должно содержать минимум 6 символов.")
        return name

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Цена товара должна быть больше 0.")
        return price
