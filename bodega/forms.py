from django import forms
from .models import Producto, MovimientoStock, Categoria, Marca

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['sku', 'nombre', 'descripcion', 'categoria', 'marca', 'precio', 'stock', 'stock_minimo', 'imagen', 'activo']
        widgets = {
            'sku': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: GTR-FEND-001'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Guitarra Eléctrica Fender Stratocaster'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'marca': forms.Select(attrs={'class': 'form-select'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '1000'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MovimientoStockForm(forms.ModelForm):
    class Meta:
        model = MovimientoStock
        fields = ['producto', 'tipo', 'cantidad', 'motivo']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Recepción de pedido #1042'}),
        }


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'slug']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre', 'pais_origen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'pais_origen': forms.TextInput(attrs={'class': 'form-control'}),
        }
