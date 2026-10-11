from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum, F, Q, ExpressionWrapper, DecimalField
from django.core.paginator import Paginator
from .models import Producto, MovimientoStock, Categoria, Marca
from .forms import ProductoForm, MovimientoStockForm, CategoriaForm, MarcaForm


def lista_productos(request):
    """
    Vista pública de catálogo de productos activos en cuadrícula de tarjetas.
    Optimizada con select_related para evitar el problema N+1 en FK de
    categoria y marca. Solo retorna productos con activo=True.
    """
    productos = (
        Producto.objects
        .select_related('categoria', 'marca')
        .filter(activo=True)
        .order_by('categoria__nombre', 'nombre')
    )
    return render(request, 'bodega/lista.html', {'productos': productos})

def dashboard(request):
    total_productos = Producto.objects.count()
    total_stock = Producto.objects.aggregate(total=Sum('stock'))['total'] or 0
    
    # Calculate inventory valuation: Sum(precio * stock)
    valor_inventario = Producto.objects.aggregate(
        valor=Sum(ExpressionWrapper(F('precio') * F('stock'), output_field=DecimalField()))
    )['valor'] or 0

    productos_bajo_stock = Producto.objects.filter(stock__lte=F('stock_minimo'), stock__gt=0).count()
    productos_sin_stock = Producto.objects.filter(stock__lte=0).count()
    
    ultimos_movimientos = MovimientoStock.objects.select_related('producto', 'usuario')[:8]
    alertas_stock = Producto.objects.filter(stock__lte=F('stock_minimo')).order_by('stock')[:6]

    context = {
        'total_productos': total_productos,
        'total_stock': total_stock,
        'valor_inventario': valor_inventario,
        'productos_bajo_stock': productos_bajo_stock,
        'productos_sin_stock': productos_sin_stock,
        'ultimos_movimientos': ultimos_movimientos,
        'alertas_stock': alertas_stock,
    }
    return render(request, 'bodega/dashboard.html', context)


def producto_list(request):
    query = request.GET.get('q', '')
    cat_id = request.GET.get('categoria', '')
    marca_id = request.GET.get('marca', '')
    estado = request.GET.get('estado', '')

    productos = Producto.objects.select_related('categoria', 'marca').all()

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
    producto = get_object_or_404(Producto.objects.select_related('categoria', 'marca'), pk=pk)
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


def categoria_list(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada con éxito.')
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    
    categorias = Categoria.objects.annotate(num_productos=Sum('productos__id')).all()
    return render(request, 'bodega/categoria_list.html', {'categorias': categorias, 'form': form})


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
