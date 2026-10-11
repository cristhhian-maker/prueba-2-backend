from django.contrib import admin
from .models import Categoria, Marca, Producto, MovimientoStock

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ('nombre',)

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais_origen')
    search_fields = ('nombre', 'pais_origen')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('sku', 'nombre', 'categoria', 'marca', 'precio', 'stock', 'stock_minimo', 'estado_stock', 'activo')
    list_filter = ('categoria', 'marca', 'activo')
    search_fields = ('sku', 'nombre', 'descripcion')
    list_editable = ('precio', 'stock', 'stock_minimo', 'activo')

@admin.register(MovimientoStock)
class MovimientoStockAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'tipo', 'producto', 'cantidad', 'motivo', 'usuario')
    list_filter = ('tipo', 'fecha')
    search_fields = ('producto__nombre', 'producto__sku', 'motivo')
