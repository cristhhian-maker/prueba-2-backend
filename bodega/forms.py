from django import forms
from .models import Producto, MovimientoStock, Categoria, Marca, Proveedor, Sucursal, Solicitud, DetalleSolicitud


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['sku', 'nombre', 'descripcion', 'categoria', 'marca', 'proveedor', 'precio', 'stock', 'stock_minimo', 'imagen', 'activo']
        widgets = {
            'sku': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: GTR-FEND-001'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Guitarra Eléctrica Fender Stratocaster'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'marca': forms.Select(attrs={'class': 'form-select'}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
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


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'rut', 'contacto', 'email', 'telefono', 'direccion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 76.123.456-7'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: +56 9 1234 5678'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ['nombre', 'direccion', 'ciudad', 'telefono', 'email', 'encargado', 'activa']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'encargado': forms.TextInput(attrs={'class': 'form-control'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['sucursal', 'observacion']
        widgets = {
            'sucursal': forms.Select(attrs={'class': 'form-select'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                 'placeholder': 'Observaciones o notas adicionales...'}),
        }


class SolicitudEstadoForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['estado', 'observacion']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DetalleSolicitudForm(forms.ModelForm):
    class Meta:
        model = DetalleSolicitud
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }


DetalleSolicitudFormSet = forms.inlineformset_factory(
    Solicitud, DetalleSolicitud,
    form=DetalleSolicitudForm,
    extra=3,
    can_delete=True,
    min_num=1,
    validate_min=True,
)
