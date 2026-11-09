from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    pais_origen = models.CharField(max_length=100, blank=True, verbose_name="País de Origen")

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150, unique=True, verbose_name="Nombre")
    rut = models.CharField(max_length=20, blank=True, verbose_name="RUT")
    contacto = models.CharField(max_length=100, blank=True, verbose_name="Persona de Contacto")
    email = models.EmailField(blank=True, verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    direccion = models.TextField(blank=True, verbose_name="Dirección")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    sku = models.CharField(max_length=50, unique=True, verbose_name="Código SKU")
    nombre = models.CharField(max_length=150, verbose_name="Nombre del Producto")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="productos", verbose_name="Categoría")
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name="productos", verbose_name="Marca")
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="productos", verbose_name="Proveedor"
    )
    precio = models.DecimalField(max_digits=12, decimal_places=0, validators=[MinValueValidator(0)], verbose_name="Precio ($)")
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="Stock Actual")
    stock_minimo = models.IntegerField(default=5, validators=[MinValueValidator(0)], verbose_name="Stock Mínimo")
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True, verbose_name="Imagen del Producto")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.sku} - {self.nombre}"

    @property
    def es_stock_bajo(self):
        return self.stock <= self.stock_minimo and self.stock > 0

    @property
    def sin_stock(self):
        return self.stock <= 0

    @property
    def estado_stock(self):
        if self.stock <= 0:
            return "Agotado"
        elif self.stock <= self.stock_minimo:
            return "Stock Bajo"
        return "Normal"


class Sucursal(models.Model):
    nombre = models.CharField(max_length=150, unique=True, verbose_name="Nombre")
    direccion = models.TextField(blank=True, verbose_name="Dirección")
    ciudad = models.CharField(max_length=100, blank=True, verbose_name="Ciudad")
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    email = models.EmailField(blank=True, verbose_name="Correo Electrónico")
    encargado = models.CharField(max_length=100, blank=True, verbose_name="Encargado")
    activa = models.BooleanField(default=True, verbose_name="Activa")

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Solicitud(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADA', 'Aprobada'),
        ('RECHAZADA', 'Rechazada'),
        ('DESPACHADA', 'Despachada'),
    ]

    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT, related_name="solicitudes", verbose_name="Sucursal")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Solicitud")
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='PENDIENTE', verbose_name="Estado")
    observacion = models.TextField(blank=True, verbose_name="Observación")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Registrado por")

    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"
        ordering = ['-fecha']

    def __str__(self):
        return f"Solicitud #{self.pk} - {self.sucursal} ({self.get_estado_display()})"

    @property
    def total_productos(self):
        return self.detalles.aggregate(total=models.Sum('cantidad'))['total'] or 0


class DetalleSolicitud(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name="detalles", verbose_name="Solicitud")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name="detalles_solicitud", verbose_name="Producto")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad Solicitada")

    class Meta:
        verbose_name = "Detalle de Solicitud"
        verbose_name_plural = "Detalles de Solicitud"
        unique_together = [['solicitud', 'producto']]

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad}"

    @property
    def subtotal(self):
        return self.producto.precio * self.cantidad


class MovimientoStock(models.Model):
    TIPO_CHOICES = [
        ('INGRESO', 'Ingreso (Entrada)'),
        ('EGRESO', 'Egreso (Salida/Venta)'),
        ('AJUSTE', 'Ajuste de Inventario'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="movimientos", verbose_name="Producto")
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, verbose_name="Tipo de Movimiento")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    motivo = models.CharField(max_length=255, help_text="Ej: Compra a proveedor, Venta a cliente, Mermas, etc.", verbose_name="Motivo / Observación")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuario responsable")
    solicitud = models.ForeignKey(
        Solicitud, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="movimientos", verbose_name="Solicitud relacionada"
    )
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")

    class Meta:
        verbose_name = "Movimiento de Stock"
        verbose_name_plural = "Movimientos de Stock"
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.producto.nombre} ({self.cantidad})"

    def save(self, *args, **kwargs):
        if not self.pk:  # New movement creation
            if self.tipo == 'INGRESO':
                self.producto.stock += self.cantidad
            elif self.tipo == 'EGRESO':
                self.producto.stock = max(0, self.producto.stock - self.cantidad)
            elif self.tipo == 'AJUSTE':
                self.producto.stock = self.cantidad
            self.producto.save()
        super().save(*args, **kwargs)
