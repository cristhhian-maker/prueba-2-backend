from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import (
    Sum, F, Q, Count, Avg,
    ExpressionWrapper, DecimalField, IntegerField
)
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta

from .models import (
    Producto, MovimientoStock, Categoria, Marca,
    Proveedor, Sucursal, Solicitud, DetalleSolicitud
)
from .forms import (
    ProductoForm, MovimientoStockForm, CategoriaForm, MarcaForm,
    ProveedorForm, SucursalForm, SolicitudForm, SolicitudEstadoForm,
    DetalleSolicitudFormSet
)


# ─────────────────────────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────────────────────────

def dashboard(request):
    total_productos = Producto.objects.count()
    total_stock = Producto.objects.aggregate(total=Sum('stock'))['total'] or 0

    valor_inventario = Producto.objects.aggregate(
        valor=Sum(ExpressionWrapper(F('precio') * F('stock'), output_field=DecimalField()))
    )['valor'] or 0

    productos_bajo_stock = Producto.objects.filter(stock__lte=F('stock_minimo'), stock__gt=0).count()
    productos_sin_stock = Producto.objects.filter(stock__lte=0).count()

    ultimos_movimientos = MovimientoStock.objects.select_related('producto', 'usuario')[:8]
    alertas_stock = Producto.objects.filter(stock__lte=F('stock_minimo')).order_by('stock')[:6]

    # Solicitudes
    solicitudes_pendientes = Solicitud.objects.filter(estado='PENDIENTE').count()
    total_solicitudes = Solicitud.objects.count()
    total_sucursales = Sucursal.objects.filter(activa=True).count()
    total_proveedores = Proveedor.objects.filter(activo=True).count()

    context = {
        'total_productos': total_productos,
        'total_stock': total_stock,
        'valor_inventario': valor_inventario,
        'productos_bajo_stock': productos_bajo_stock,
        'productos_sin_stock': productos_sin_stock,
        'ultimos_movimientos': ultimos_movimientos,
        'alertas_stock': alertas_stock,
        'solicitudes_pendientes': solicitudes_pendientes,
        'total_solicitudes': total_solicitudes,
        'total_sucursales': total_sucursales,
        'total_proveedores': total_proveedores,
    }
    return render(request, 'bodega/dashboard.html', context)


# ─────────────────────────────────────────────────────────────────
# CATÁLOGO PÚBLICO
# ─────────────────────────────────────────────────────────────────

def lista_productos(request):
    productos = (
        Producto.objects
        .select_related('categoria', 'marca')
        .filter(activo=True)
        .order_by('categoria__nombre', 'nombre')
    )
    return render(request, 'bodega/lista.html', {'productos': productos})


# ─────────────────────────────────────────────────────────────────
# PRODUCTOS
# ─────────────────────────────────────────────────────────────────

def producto_list(request):
    query = request.GET.get('q', '')
    cat_id = request.GET.get('categoria', '')
    marca_id = request.GET.get('marca', '')
    estado = request.GET.get('estado', '')

    productos = Producto.objects.select_related('categoria', 'marca', 'proveedor').all()

    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(sku__icontains=query) | Q(descripcion__icontains=query)
        )
    if cat_id:
        productos = productos.filter(categoria_id=cat_id)
    if marca_id:
        productos = productos.filter(marca_id=marca_id)
    if estado == 'bajo':
        productos = productos.filter(stock__lte=F('stock_minimo'), stock__gt=0)
    elif estado == 'agotado':
        productos = productos.filter(stock__lte=0)
    elif estado == 'ok':
        productos = productos.filter(stock__gt=F('stock_minimo'))

    paginator = Paginator(productos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()

    context = {
        'page_obj': page_obj,
        'query': query,
        'categorias': categorias,
        'marcas': marcas,
        'selected_cat': cat_id,
        'selected_marca': marca_id,
        'selected_estado': estado,
    }
    return render(request, 'bodega/producto_list.html', context)


def producto_detail(request, pk):
    producto = get_object_or_404(Producto.objects.select_related('categoria', 'marca', 'proveedor'), pk=pk)
    movimientos = producto.movimientos.select_related('usuario').all()[:15]
    return render(request, 'bodega/producto_detail.html', {'producto': producto, 'movimientos': movimientos})


def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" registrado exitosamente.')
            return redirect('producto_detail', pk=producto.pk)
    else:
        form = ProductoForm()
    return render(request, 'bodega/producto_form.html', {'form': form, 'titulo': 'Nuevo Producto'})


def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado correctamente.')
            return redirect('producto_detail', pk=producto.pk)
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'bodega/producto_form.html', {'form': form, 'titulo': f'Editar Producto: {producto.nombre}', 'producto': producto})


def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'El producto "{nombre}" ha sido eliminado.')
        return redirect('producto_list')
    return render(request, 'bodega/producto_confirm_delete.html', {'producto': producto})


# ─────────────────────────────────────────────────────────────────
# MOVIMIENTOS DE STOCK
# ─────────────────────────────────────────────────────────────────

def movimiento_list(request):
    movimientos = MovimientoStock.objects.select_related('producto', 'usuario').all()
    paginator = Paginator(movimientos, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'bodega/movimiento_list.html', {'page_obj': page_obj})


def movimiento_create(request):
    if request.method == 'POST':
        form = MovimientoStockForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            if request.user.is_authenticated:
                movimiento.usuario = request.user
            movimiento.save()
            messages.success(request, f'Movimiento de stock registrado correctamente para {movimiento.producto.nombre}.')
            return redirect('movimiento_list')
    else:
        producto_id = request.GET.get('producto')
        initial = {}
        if producto_id:
            initial['producto'] = producto_id
        form = MovimientoStockForm(initial=initial)
    return render(request, 'bodega/movimiento_form.html', {'form': form})


# ─────────────────────────────────────────────────────────────────
# CATEGORÍAS
# ─────────────────────────────────────────────────────────────────

def categoria_list(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada con éxito.')
            return redirect('categoria_list')
    else:
        form = CategoriaForm()

    categorias = Categoria.objects.annotate(num_productos=Count('productos')).all()
    return render(request, 'bodega/categoria_list.html', {'categorias': categorias, 'form': form})


# ─────────────────────────────────────────────────────────────────
# MARCAS
# ─────────────────────────────────────────────────────────────────

def marca_list(request):
    if request.method == 'POST':
        form = MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marca registrada con éxito.')
            return redirect('marca_list')
    else:
        form = MarcaForm()

    marcas = Marca.objects.all()
    return render(request, 'bodega/marca_list.html', {'marcas': marcas, 'form': form})


# ─────────────────────────────────────────────────────────────────
# PROVEEDORES
# ─────────────────────────────────────────────────────────────────

def proveedor_list(request):
    proveedores = Proveedor.objects.annotate(num_productos=Count('productos')).all()
    return render(request, 'bodega/proveedor_list.html', {'proveedores': proveedores})


def proveedor_create(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            prov = form.save()
            messages.success(request, f'Proveedor "{prov.nombre}" registrado con éxito.')
            return redirect('proveedor_list')
    else:
        form = ProveedorForm()
    return render(request, 'bodega/proveedor_form.html', {'form': form, 'titulo': 'Nuevo Proveedor'})


def proveedor_update(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, f'Proveedor "{proveedor.nombre}" actualizado.')
            return redirect('proveedor_list')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'bodega/proveedor_form.html', {'form': form, 'titulo': f'Editar: {proveedor.nombre}', 'proveedor': proveedor})


def proveedor_delete(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        nombre = proveedor.nombre
        proveedor.delete()
        messages.success(request, f'Proveedor "{nombre}" eliminado.')
        return redirect('proveedor_list')
    return render(request, 'bodega/proveedor_confirm_delete.html', {'proveedor': proveedor})


# ─────────────────────────────────────────────────────────────────
# SUCURSALES
# ─────────────────────────────────────────────────────────────────

def sucursal_list(request):
    sucursales = Sucursal.objects.annotate(num_solicitudes=Count('solicitudes')).all()
    return render(request, 'bodega/sucursal_list.html', {'sucursales': sucursales})


def sucursal_create(request):
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            suc = form.save()
            messages.success(request, f'Sucursal "{suc.nombre}" registrada con éxito.')
            return redirect('sucursal_list')
    else:
        form = SucursalForm()
    return render(request, 'bodega/sucursal_form.html', {'form': form, 'titulo': 'Nueva Sucursal'})


def sucursal_update(request, pk):
    sucursal = get_object_or_404(Sucursal, pk=pk)
    if request.method == 'POST':
        form = SucursalForm(request.POST, instance=sucursal)
        if form.is_valid():
            form.save()
            messages.success(request, f'Sucursal "{sucursal.nombre}" actualizada.')
            return redirect('sucursal_list')
    else:
        form = SucursalForm(instance=sucursal)
    return render(request, 'bodega/sucursal_form.html', {'form': form, 'titulo': f'Editar: {sucursal.nombre}', 'sucursal': sucursal})


def sucursal_delete(request, pk):
    sucursal = get_object_or_404(Sucursal, pk=pk)
    if request.method == 'POST':
        nombre = sucursal.nombre
        sucursal.delete()
        messages.success(request, f'Sucursal "{nombre}" eliminada.')
        return redirect('sucursal_list')
    return render(request, 'bodega/sucursal_confirm_delete.html', {'sucursal': sucursal})


# ─────────────────────────────────────────────────────────────────
# SOLICITUDES
# ─────────────────────────────────────────────────────────────────

def solicitud_list(request):
    estado = request.GET.get('estado', '')
    sucursal_id = request.GET.get('sucursal', '')

    solicitudes = Solicitud.objects.select_related('sucursal', 'usuario').annotate(
        total_items=Sum('detalles__cantidad')
    ).order_by('-fecha')

    if estado:
        solicitudes = solicitudes.filter(estado=estado)
    if sucursal_id:
        solicitudes = solicitudes.filter(sucursal_id=sucursal_id)

    paginator = Paginator(solicitudes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    sucursales = Sucursal.objects.all()
    context = {
        'page_obj': page_obj,
        'sucursales': sucursales,
        'selected_estado': estado,
        'selected_sucursal': sucursal_id,
        'estado_choices': Solicitud.ESTADO_CHOICES,
    }
    return render(request, 'bodega/solicitud_list.html', context)


def solicitud_detail(request, pk):
    solicitud = get_object_or_404(
        Solicitud.objects.select_related('sucursal', 'usuario'),
        pk=pk
    )
    detalles = solicitud.detalles.select_related('producto__categoria', 'producto__marca').all()
    return render(request, 'bodega/solicitud_detail.html', {
        'solicitud': solicitud,
        'detalles': detalles,
    })


def solicitud_create(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        formset = DetalleSolicitudFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            solicitud = form.save(commit=False)
            if request.user.is_authenticated:
                solicitud.usuario = request.user
            solicitud.save()
            formset.instance = solicitud
            formset.save()
            messages.success(request, f'Solicitud #{solicitud.pk} creada correctamente para {solicitud.sucursal}.')
            return redirect('solicitud_detail', pk=solicitud.pk)
    else:
        form = SolicitudForm()
        formset = DetalleSolicitudFormSet()
    return render(request, 'bodega/solicitud_form.html', {
        'form': form,
        'formset': formset,
        'titulo': 'Nueva Solicitud',
    })


def solicitud_update_estado(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk)
    if request.method == 'POST':
        form = SolicitudEstadoForm(request.POST, instance=solicitud)
        if form.is_valid():
            sol = form.save()
            # Si se despacha, generar movimientos EGRESO automáticamente
            if sol.estado == 'DESPACHADA':
                for detalle in sol.detalles.select_related('producto').all():
                    MovimientoStock.objects.create(
                        producto=detalle.producto,
                        tipo='EGRESO',
                        cantidad=detalle.cantidad,
                        motivo=f'Despacho solicitud #{sol.pk} - {sol.sucursal}',
                        usuario=request.user if request.user.is_authenticated else None,
                        solicitud=sol,
                    )
                messages.success(request, f'Solicitud #{sol.pk} despachada. Stock actualizado automáticamente.')
            else:
                messages.success(request, f'Estado de solicitud #{sol.pk} actualizado a "{sol.get_estado_display()}".')
            return redirect('solicitud_detail', pk=sol.pk)
    else:
        form = SolicitudEstadoForm(instance=solicitud)
    return render(request, 'bodega/solicitud_estado_form.html', {
        'form': form,
        'solicitud': solicitud,
    })


def solicitud_delete(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk)
    if solicitud.estado != 'PENDIENTE':
        messages.error(request, 'Solo se pueden eliminar solicitudes en estado Pendiente.')
        return redirect('solicitud_detail', pk=pk)
    if request.method == 'POST':
        solicitud.delete()
        messages.success(request, f'Solicitud #{pk} eliminada.')
        return redirect('solicitud_list')
    return render(request, 'bodega/solicitud_confirm_delete.html', {'solicitud': solicitud})


# ─────────────────────────────────────────────────────────────────
# REPORTES
# ─────────────────────────────────────────────────────────────────

def reportes_index(request):
    """Índice de los 20 reportes."""
    return render(request, 'bodega/reportes/index.html')


# R1 – Todos los productos registrados
def reporte_1(request):
    productos = Producto.objects.select_related('categoria', 'marca', 'proveedor').order_by('nombre')
    return render(request, 'bodega/reportes/reporte_01.html', {'productos': productos})


# R2 – Productos por categoría seleccionada
def reporte_2(request):
    categorias = Categoria.objects.all()
    cat_id = request.GET.get('categoria', '')
    productos = []
    categoria_sel = None
    if cat_id:
        categoria_sel = get_object_or_404(Categoria, pk=cat_id)
        productos = Producto.objects.select_related('marca').filter(categoria=categoria_sel).order_by('nombre')
    return render(request, 'bodega/reportes/reporte_02.html', {
        'categorias': categorias,
        'productos': productos,
        'categoria_sel': categoria_sel,
        'cat_id': cat_id,
    })


# R3 – Productos con stock bajo el mínimo
def reporte_3(request):
    productos = (
        Producto.objects
        .select_related('categoria', 'marca')
        .filter(stock__lte=F('stock_minimo'))
        .order_by('stock')
    )
    return render(request, 'bodega/reportes/reporte_03.html', {'productos': productos})


# R4 – Top 10 productos con mayor precio
def reporte_4(request):
    productos = (
        Producto.objects
        .select_related('categoria', 'marca')
        .order_by('-precio')[:10]
    )
    return render(request, 'bodega/reportes/reporte_04.html', {'productos': productos})


# R5 – Cantidad de productos por categoría
def reporte_5(request):
    categorias = (
        Categoria.objects
        .annotate(total=Count('productos'))
        .order_by('-total')
    )
    return render(request, 'bodega/reportes/reporte_05.html', {'categorias': categorias})


# R6 – Productos de un proveedor seleccionado
def reporte_6(request):
    proveedores = Proveedor.objects.all()
    prov_id = request.GET.get('proveedor', '')
    productos = []
    proveedor_sel = None
    if prov_id:
        proveedor_sel = get_object_or_404(Proveedor, pk=prov_id)
        productos = Producto.objects.select_related('categoria', 'marca').filter(proveedor=proveedor_sel).order_by('nombre')
    return render(request, 'bodega/reportes/reporte_06.html', {
        'proveedores': proveedores,
        'productos': productos,
        'proveedor_sel': proveedor_sel,
        'prov_id': prov_id,
    })


# R7 – Solicitudes de una sucursal específica
def reporte_7(request):
    sucursales = Sucursal.objects.all()
    suc_id = request.GET.get('sucursal', '')
    solicitudes = []
    sucursal_sel = None
    if suc_id:
        sucursal_sel = get_object_or_404(Sucursal, pk=suc_id)
        solicitudes = (
            Solicitud.objects
            .filter(sucursal=sucursal_sel)
            .annotate(total_items=Sum('detalles__cantidad'))
            .order_by('-fecha')
        )
    return render(request, 'bodega/reportes/reporte_07.html', {
        'sucursales': sucursales,
        'solicitudes': solicitudes,
        'sucursal_sel': sucursal_sel,
        'suc_id': suc_id,
    })


# R8 – Productos y cantidades de una solicitud seleccionada
def reporte_8(request):
    solicitudes = Solicitud.objects.select_related('sucursal').all()
    sol_id = request.GET.get('solicitud', '')
    detalles = []
    solicitud_sel = None
    if sol_id:
        solicitud_sel = get_object_or_404(Solicitud.objects.select_related('sucursal'), pk=sol_id)
        detalles = solicitud_sel.detalles.select_related('producto__categoria').all()
    return render(request, 'bodega/reportes/reporte_08.html', {
        'solicitudes': solicitudes,
        'detalles': detalles,
        'solicitud_sel': solicitud_sel,
        'sol_id': sol_id,
    })


# R9 – Conteo de solicitudes por estado
def reporte_9(request):
    resumen = (
        Solicitud.objects
        .values('estado')
        .annotate(total=Count('id'))
        .order_by('estado')
    )
    # Mapa de etiquetas
    etiquetas = dict(Solicitud.ESTADO_CHOICES)
    for item in resumen:
        item['estado_display'] = etiquetas.get(item['estado'], item['estado'])

    total = Solicitud.objects.count()
    return render(request, 'bodega/reportes/reporte_09.html', {
        'resumen': resumen,
        'total': total,
    })


# R10 – Solicitudes en un rango de fechas
def reporte_10(request):
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    solicitudes = []
    if fecha_desde and fecha_hasta:
        solicitudes = (
            Solicitud.objects
            .select_related('sucursal')
            .filter(fecha__date__gte=fecha_desde, fecha__date__lte=fecha_hasta)
            .annotate(total_items=Sum('detalles__cantidad'))
            .order_by('-fecha')
        )
    return render(request, 'bodega/reportes/reporte_10.html', {
        'solicitudes': solicitudes,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
    })


# R11 – Top 5 sucursales con mayor cantidad de productos solicitados
def reporte_11(request):
    sucursales = (
        Sucursal.objects
        .annotate(total_solicitado=Sum('solicitudes__detalles__cantidad'))
        .filter(total_solicitado__isnull=False)
        .order_by('-total_solicitado')[:5]
    )
    return render(request, 'bodega/reportes/reporte_11.html', {'sucursales': sucursales})


# R12 – Productos más solicitados por sucursales
def reporte_12(request):
    productos = (
        Producto.objects
        .annotate(total_solicitado=Sum('detalles_solicitud__cantidad'))
        .filter(total_solicitado__isnull=False)
        .order_by('-total_solicitado')
        .select_related('categoria')
    )
    return render(request, 'bodega/reportes/reporte_12.html', {'productos': productos})


# R13 – Proveedor que suministra más productos diferentes
def reporte_13(request):
    proveedores = (
        Proveedor.objects
        .annotate(total_productos=Count('productos'))
        .order_by('-total_productos')
    )
    return render(request, 'bodega/reportes/reporte_13.html', {'proveedores': proveedores})


# R14 – Valor total del inventario
def reporte_14(request):
    productos = (
        Producto.objects
        .select_related('categoria')
        .annotate(
            valor=ExpressionWrapper(F('precio') * F('stock'), output_field=DecimalField())
        )
        .order_by('-valor')
    )
    valor_total = productos.aggregate(total=Sum('valor'))['total'] or 0
    return render(request, 'bodega/reportes/reporte_14.html', {
        'productos': productos,
        'valor_total': valor_total,
    })


# R15 – Productos no solicitados por ninguna sucursal
def reporte_15(request):
    productos = (
        Producto.objects
        .select_related('categoria', 'marca')
        .filter(detalles_solicitud__isnull=True)
        .order_by('nombre')
    )
    return render(request, 'bodega/reportes/reporte_15.html', {'productos': productos})


# R16 – Unidades salidas durante el último mes
def reporte_16(request):
    hace_un_mes = timezone.now() - timedelta(days=30)
    movimientos = (
        MovimientoStock.objects
        .filter(tipo='EGRESO', fecha__gte=hace_un_mes)
        .values('producto__id', 'producto__nombre', 'producto__sku')
        .annotate(total_salidas=Sum('cantidad'))
        .order_by('-total_salidas')
    )
    return render(request, 'bodega/reportes/reporte_16.html', {
        'movimientos': movimientos,
        'hace_un_mes': hace_un_mes,
    })


# R17 – Sucursales con solicitudes pendientes
def reporte_17(request):
    sucursales = (
        Sucursal.objects
        .filter(solicitudes__estado='PENDIENTE')
        .annotate(solicitudes_pendientes=Count('solicitudes', filter=Q(solicitudes__estado='PENDIENTE')))
        .distinct()
        .order_by('-solicitudes_pendientes')
    )
    return render(request, 'bodega/reportes/reporte_17.html', {'sucursales': sucursales})


# R18 – Categoría con mayor valor económico del inventario
def reporte_18(request):
    categorias = (
        Categoria.objects
        .annotate(
            valor_total=Sum(
                ExpressionWrapper(
                    F('productos__precio') * F('productos__stock'),
                    output_field=DecimalField()
                )
            )
        )
        .filter(valor_total__isnull=False)
        .order_by('-valor_total')
    )
    return render(request, 'bodega/reportes/reporte_18.html', {'categorias': categorias})


# R19 – Promedio de productos solicitados por solicitud
def reporte_19(request):
    solicitudes = (
        Solicitud.objects
        .annotate(total_por_solicitud=Sum('detalles__cantidad'))
        .filter(total_por_solicitud__isnull=False)
        .select_related('sucursal')
        .order_by('-total_por_solicitud')
    )
    promedio = solicitudes.aggregate(prom=Avg('total_por_solicitud'))['prom'] or 0
    return render(request, 'bodega/reportes/reporte_19.html', {
        'solicitudes': solicitudes,
        'promedio': promedio,
    })


# R20 – Top 5 productos más solicitados en un período
def reporte_20(request):
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    productos = []
    if fecha_desde and fecha_hasta:
        productos = (
            Producto.objects
            .filter(
                detalles_solicitud__solicitud__fecha__date__gte=fecha_desde,
                detalles_solicitud__solicitud__fecha__date__lte=fecha_hasta,
            )
            .annotate(total_solicitado=Sum('detalles_solicitud__cantidad'))
            .select_related('categoria')
            .order_by('-total_solicitado')[:5]
        )
    return render(request, 'bodega/reportes/reporte_20.html', {
        'productos': productos,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
    })
