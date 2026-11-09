from django.contrib import admin
from .models import Categoria, Marca, Producto, MovimientoStock, Proveedor, Sucursal, Solicitud, DetalleSolicitud


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ('nombre',)


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais_origen')
    search_fields = ('nombre', 'pais_origen')


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rut', 'contacto', 'telefono', 'email', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'rut', 'contacto')


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciudad', 'encargado', 'telefono', 'activa')
    list_filter = ('activa', 'ciudad')
    search_fields = ('nombre', 'ciudad', 'encargado')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('sku', 'nombre', 'categoria', 'marca', 'proveedor', 'precio', 'stock', 'stock_minimo', 'estado_stock', 'activo')
    list_filter = ('categoria', 'marca', 'proveedor', 'activo')
    search_fields = ('sku', 'nombre', 'descripcion')
    list_editable = ('precio', 'stock', 'stock_minimo', 'activo')


class DetalleSolicitudInline(admin.TabularInline):
    model = DetalleSolicitud
    extra = 1


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'sucursal', 'fecha', 'estado', 'usuario')
    list_filter = ('estado', 'fecha', 'sucursal')
    search_fields = ('sucursal__nombre', 'observacion')
    inlines = [DetalleSolicitudInline]


@admin.register(MovimientoStock)
class MovimientoStockAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'tipo', 'producto', 'cantidad', 'motivo', 'usuario', 'solicitud')
    list_filter = ('tipo', 'fecha')
    search_fields = ('producto__nombre', 'producto__sku', 'motivo')
