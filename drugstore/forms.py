from django.forms import ModelForm, ValidationError
from .models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at', 'slug')

    def clean(self):
        slug = self.cleaned_data.get('name').lower().replace(" ", '-')
        if Product.objects.filter(slug=slug).exists():
            raise ValidationError('Product with such name already exists!')
        return self.cleaned_data