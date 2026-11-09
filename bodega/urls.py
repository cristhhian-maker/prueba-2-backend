from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('catalogo/', views.lista_productos, name='lista_productos'),

    # Productos
    path('productos/', views.producto_list, name='producto_list'),
    path('productos/nuevo/', views.producto_create, name='producto_create'),
    path('productos/<int:pk>/', views.producto_detail, name='producto_detail'),
    path('productos/<int:pk>/editar/', views.producto_update, name='producto_update'),
    path('productos/<int:pk>/eliminar/', views.producto_delete, name='producto_delete'),

    # Movimientos de Stock
    path('movimientos/', views.movimiento_list, name='movimiento_list'),
    path('movimientos/nuevo/', views.movimiento_create, name='movimiento_create'),

    # Categorías y Marcas
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('marcas/', views.marca_list, name='marca_list'),

    # Proveedores
    path('proveedores/', views.proveedor_list, name='proveedor_list'),
    path('proveedores/nuevo/', views.proveedor_create, name='proveedor_create'),
    path('proveedores/<int:pk>/editar/', views.proveedor_update, name='proveedor_update'),
    path('proveedores/<int:pk>/eliminar/', views.proveedor_delete, name='proveedor_delete'),

    # Sucursales
    path('sucursales/', views.sucursal_list, name='sucursal_list'),
    path('sucursales/nueva/', views.sucursal_create, name='sucursal_create'),
    path('sucursales/<int:pk>/editar/', views.sucursal_update, name='sucursal_update'),
    path('sucursales/<int:pk>/eliminar/', views.sucursal_delete, name='sucursal_delete'),

    # Solicitudes
    path('solicitudes/', views.solicitud_list, name='solicitud_list'),
    path('solicitudes/nueva/', views.solicitud_create, name='solicitud_create'),
    path('solicitudes/<int:pk>/', views.solicitud_detail, name='solicitud_detail'),
    path('solicitudes/<int:pk>/estado/', views.solicitud_update_estado, name='solicitud_update_estado'),
    path('solicitudes/<int:pk>/eliminar/', views.solicitud_delete, name='solicitud_delete'),

    # Reportes
    path('reportes/', views.reportes_index, name='reportes_index'),
    path('reportes/01/', views.reporte_1, name='reporte_1'),
    path('reportes/02/', views.reporte_2, name='reporte_2'),
    path('reportes/03/', views.reporte_3, name='reporte_3'),
    path('reportes/04/', views.reporte_4, name='reporte_4'),
    path('reportes/05/', views.reporte_5, name='reporte_5'),
    path('reportes/06/', views.reporte_6, name='reporte_6'),
    path('reportes/07/', views.reporte_7, name='reporte_7'),
    path('reportes/08/', views.reporte_8, name='reporte_8'),
    path('reportes/09/', views.reporte_9, name='reporte_9'),
    path('reportes/10/', views.reporte_10, name='reporte_10'),
    path('reportes/11/', views.reporte_11, name='reporte_11'),
    path('reportes/12/', views.reporte_12, name='reporte_12'),
    path('reportes/13/', views.reporte_13, name='reporte_13'),
    path('reportes/14/', views.reporte_14, name='reporte_14'),
    path('reportes/15/', views.reporte_15, name='reporte_15'),
    path('reportes/16/', views.reporte_16, name='reporte_16'),
    path('reportes/17/', views.reporte_17, name='reporte_17'),
    path('reportes/18/', views.reporte_18, name='reporte_18'),
    path('reportes/19/', views.reporte_19, name='reporte_19'),
    path('reportes/20/', views.reporte_20, name='reporte_20'),
]
