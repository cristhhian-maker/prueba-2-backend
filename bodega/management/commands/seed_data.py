from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from bodega.models import (
    Categoria, Marca, Proveedor, Sucursal,
    Producto, Solicitud, DetalleSolicitud, MovimientoStock
)

class Command(BaseCommand):
    help = 'Puebla la base de datos con información completa para Bodega: Proveedores, Sucursales, Productos, Solicitudes y Movimientos'

    def handle(self, *args, **options):
        self.stdout.write("Poblando datos de Bodega...")

        # 1. Categorías
        cats = [
            {'nombre': 'Tecnología y Audio', 'slug': 'tecnologia-y-audio', 'descripcion': 'Equipos de audio, grabación, interfaces y accesorios tecnológicos'},
            {'nombre': 'Instrumentos de Cuerda', 'slug': 'instrumentos-de-cuerda', 'descripcion': 'Guitarras, bajos, ukeleles y accesorios'},
            {'nombre': 'Teclados y Pianos', 'slug': 'teclados-y-pianos', 'descripcion': 'Pianos digitales, sintetizadores y teclados controladores'},
            {'nombre': 'Percusión y Baterías', 'slug': 'percusion-y-baterias', 'descripcion': 'Baterías acústicas y electrónicas, percusión menor'},
            {'nombre': 'Amplificación', 'slug': 'amplificacion', 'descripcion': 'Amplificadores valvulares, digitales y cajas acústicas'},
            {'nombre': 'Mobiliario y Accesorios', 'slug': 'mobiliario-y-accesorios', 'descripcion': 'Atriles, banquetas, soportes y racks'},
        ]
        cat_objs = {}
        for c in cats:
            obj, _ = Categoria.objects.get_or_create(slug=c['slug'], defaults=c)
            cat_objs[c['slug']] = obj

        # 2. Marcas
        marcas = [
            {'nombre': 'Fender', 'pais_origen': 'EE.UU.'},
            {'nombre': 'Gibson', 'pais_origen': 'EE.UU.'},
            {'nombre': 'Yamaha', 'pais_origen': 'Japón'},
            {'nombre': 'Roland', 'pais_origen': 'Japón'},
            {'nombre': 'Shure', 'pais_origen': 'EE.UU.'},
            {'nombre': 'Marshall', 'pais_origen': 'Reino Unido'},
            {'nombre': 'Boss', 'pais_origen': 'Japón'},
            {'nombre': 'Pearl', 'pais_origen': 'Japón'},
            {'nombre': 'Audio-Technica', 'pais_origen': 'Japón'},
            {'nombre': 'Korg', 'pais_origen': 'Japón'},
        ]
        marca_objs = {}
        for m in marcas:
            obj, _ = Marca.objects.get_or_create(nombre=m['nombre'], defaults=m)
            marca_objs[m['nombre']] = obj

        # 3. Proveedores
        proveedores_data = [
            {
                'nombre': 'Importadora Musical Andina SpA',
                'rut': '76.845.120-3',
                'contacto': 'Carlos Contreras',
                'email': 'ventas@importandina.cl',
                'telefono': '+56 9 8456 1234',
                'direccion': 'Av. Providencia 1240, Santiago',
            },
            {
                'nombre': 'Distribuidora Global Sound S.A.',
                'rut': '77.102.455-8',
                'contacto': 'Mariana Valenzuela',
                'email': 'contacto@globalsound.cl',
                'telefono': '+56 9 7890 3412',
                'direccion': 'San Diego 890, Santiago Centro',
            },
            {
                'nombre': 'ProAudio Instruments Chile',
                'rut': '76.332.990-1',
                'contacto': 'Rodrigo Soto',
                'email': 'rsoto@proaudiochile.com',
                'telefono': '+56 9 5541 2309',
                'direccion': 'Camino Melipilla 450, Maipú',
            },
            {
                'nombre': 'Instrumentos del Pacífico Ltda.',
                'rut': '78.504.223-K',
                'contacto': 'Camila Arancibia',
                'email': 'pedidos@pacificsound.cl',
                'telefono': '+56 9 9123 4567',
                'direccion': 'Av. Libertad 340, Viña del Mar',
            },
            {
                'nombre': 'ElectroMusic Soluciones Limitada',
                'rut': '76.990.114-2',
                'contacto': 'Ignacio Vega',
                'email': 'ivega@electromusic.cl',
                'telefono': '+56 9 6654 3210',
                'direccion': 'Barros Arana 560, Concepción',
            },
        ]
        prov_objs = {}
        for p in proveedores_data:
            obj, _ = Proveedor.objects.get_or_create(nombre=p['nombre'], defaults=p)
            prov_objs[p['nombre']] = obj

        # 4. Sucursales
        sucursales_data = [
            {
                'nombre': 'Sucursal Santiago Centro',
                'direccion': 'Paseo Ahumada 250, Local 14',
                'ciudad': 'Santiago',
                'telefono': '+56 2 2698 1122',
                'email': 'stgocentro@bodegaempresa.cl',
                'encargado': 'Mauricio Palma',
            },
            {
                'nombre': 'Sucursal Providencia',
                'direccion': 'Av. Nueva Providencia 2155',
                'ciudad': 'Santiago',
                'telefono': '+56 2 2234 5566',
                'email': 'providencia@bodegaempresa.cl',
                'encargado': 'Daniela Morales',
            },
            {
                'nombre': 'Sucursal Maipú',
                'direccion': 'Av. Pajaritos 1890',
                'ciudad': 'Santiago',
                'telefono': '+56 2 2531 9988',
                'email': 'maipu@bodegaempresa.cl',
                'encargado': 'Sebastián Reyes',
            },
            {
                'nombre': 'Sucursal Viña del Mar',
                'direccion': 'Calle Valparaíso 680',
                'ciudad': 'Viña del Mar',
                'telefono': '+56 32 268 4400',
                'email': 'vinadelmar@bodegaempresa.cl',
                'encargado': 'Patricia Gómez',
            },
            {
                'nombre': 'Sucursal Concepción Centro',
                'direccion': 'Calle O\'Higgins 450',
                'ciudad': 'Concepción',
                'telefono': '+56 41 222 3344',
                'email': 'concepcion@bodegaempresa.cl',
                'encargado': 'Felipe Araya',
            },
            {
                'nombre': 'Sucursal Antofagasta',
                'direccion': 'Calle Prat 780',
                'ciudad': 'Antofagasta',
                'telefono': '+56 55 234 1100',
                'email': 'antofagasta@bodegaempresa.cl',
                'encargado': 'Claudia Rojas',
            },
        ]
        suc_objs = {}
        for s in sucursales_data:
            obj, _ = Sucursal.objects.get_or_create(nombre=s['nombre'], defaults=s)
            suc_objs[s['nombre']] = obj

        # 5. Productos
        productos_data = [
            {
                'sku': 'GTR-FEND-STRAT-01',
                'nombre': 'Fender Player Stratocaster MN 3TS',
                'descripcion': 'Guitarra eléctrica icónica Fender pastillas Player Series Single-Coil.',
                'categoria': cat_objs['instrumentos-de-cuerda'],
                'marca': marca_objs['Fender'],
                'proveedor': prov_objs['Importadora Musical Andina SpA'],
                'precio': 899000,
                'stock': 14,
                'stock_minimo': 5,
            },
            {
                'sku': 'GTR-GIBS-LES-01',
                'nombre': 'Gibson Les Paul Standard 50s Heritage Cherry',
                'descripcion': 'Cuerpo de caoba maciza con tapa de arce figurado AA.',
                'categoria': cat_objs['instrumentos-de-cuerda'],
                'marca': marca_objs['Gibson'],
                'proveedor': prov_objs['Importadora Musical Andina SpA'],
                'precio': 2490000,
                'stock': 2,
                'stock_minimo': 3,  # Stock bajo
            },
            {
                'sku': 'TEC-YAMA-P125',
                'nombre': 'Yamaha P-125B Piano Digital 88 Teclas',
                'descripcion': 'Piano digital con contrapeso Graded Hammer Standard.',
                'categoria': cat_objs['teclados-y-pianos'],
                'marca': marca_objs['Yamaha'],
                'proveedor': prov_objs['Distribuidora Global Sound S.A.'],
                'precio': 649000,
                'stock': 8,
                'stock_minimo': 4,
            },
            {
                'sku': 'TEC-ROLA-JUNO',
                'nombre': 'Roland JUNO-DS61 Sintetizador Portátil',
                'descripcion': 'Sintetizador versátil de 61 teclas con voces pro.',
                'categoria': cat_objs['teclados-y-pianos'],
                'marca': marca_objs['Roland'],
                'proveedor': prov_objs['Distribuidora Global Sound S.A.'],
                'precio': 789000,
                'stock': 1,
                'stock_minimo': 3,  # Stock bajo
            },
            {
                'sku': 'BAT-PEAR-ROAD-01',
                'nombre': 'Pearl Roadshow RS525 Batería Acústica 5 Cuerpos',
                'descripcion': 'Set completo de batería acústica incluye atriles y platillos.',
                'categoria': cat_objs['percusion-y-baterias'],
                'marca': marca_objs['Pearl'],
                'proveedor': prov_objs['ProAudio Instruments Chile'],
                'precio': 599000,
                'stock': 0,
                'stock_minimo': 2,  # Agotado
            },
            {
                'sku': 'AUD-SHUR-SM58',
                'nombre': 'Shure SM58-LC Micrófono Dinámico Vocal',
                'descripcion': 'Estándar mundial para presentaciones vocales en vivo.',
                'categoria': cat_objs['tecnologia-y-audio'],
                'marca': marca_objs['Shure'],
                'proveedor': prov_objs['ProAudio Instruments Chile'],
                'precio': 119000,
                'stock': 35,
                'stock_minimo': 10,
            },
            {
                'sku': 'AUD-AT-M50X',
                'nombre': 'Audio-Technica ATH-M50x Auriculares de Monitoreo',
                'descripcion': 'Auriculares profesionales aclamados para mezcla en estudio.',
                'categoria': cat_objs['tecnologia-y-audio'],
                'marca': marca_objs['Audio-Technica'],
                'proveedor': prov_objs['ProAudio Instruments Chile'],
                'precio': 169000,
                'stock': 22,
                'stock_minimo': 6,
            },
            {
                'sku': 'AMP-MARS-DSL40',
                'nombre': 'Marshall DSL40CR Combo Valvular 40W',
                'descripcion': 'Amplificador combo 1x12 Celestion V-Type.',
                'categoria': cat_objs['amplificacion'],
                'marca': marca_objs['Marshall'],
                'proveedor': prov_objs['ElectroMusic Soluciones Limitada'],
                'precio': 849000,
                'stock': 3,
                'stock_minimo': 4,  # Stock bajo
            },
            {
                'sku': 'AMP-BOSS-KAT50',
                'nombre': 'Boss Katana-50 MkII Amplificador Guitarra',
                'descripcion': 'Combo 50 vatios 1x12 con 5 caracteres tonales.',
                'categoria': cat_objs['amplificacion'],
                'marca': marca_objs['Boss'],
                'proveedor': prov_objs['ElectroMusic Soluciones Limitada'],
                'precio': 299000,
                'stock': 18,
                'stock_minimo': 5,
            },
            {
                'sku': 'TEC-KORG-MINILOG',
                'nombre': 'Korg Minilogue XD Sintetizador Analógico Polifónico',
                'descripcion': 'Sintetizador híbrido analógico/digital de 4 voces.',
                'categoria': cat_objs['teclados-y-pianos'],
                'marca': marca_objs['Korg'],
                'proveedor': prov_objs['Distribuidora Global Sound S.A.'],
                'precio': 689000,
                'stock': 6,
                'stock_minimo': 3,
            },
            {
                'sku': 'MOB-ATRIL-PRO-01',
                'nombre': 'Atril de Partitura Profesional Ajustable Reforzado',
                'descripcion': 'Atril de metal pesado con estuche para transporte.',
                'categoria': cat_objs['mobiliario-y-accesorios'],
                'marca': marca_objs['Yamaha'],
                'proveedor': prov_objs['Instrumentos del Pacífico Ltda.'],
                'precio': 28900,
                'stock': 40,
                'stock_minimo': 10,
            },
            {
                'sku': 'MOB-SOP-GTR-01',
                'nombre': 'Soporte Universal de Piso para Guitarra o Bajo',
                'descripcion': 'Soporte plegable acolchado con bloqueo de mástil.',
                'categoria': cat_objs['mobiliario-y-accesorios'],
                'marca': marca_objs['Fender'],
                'proveedor': prov_objs['Instrumentos del Pacífico Ltda.'],
                'precio': 19900,
                'stock': 55,
                'stock_minimo': 15,
            },
            {
                'sku': 'ACC-CABLE-PRO-01',
                'nombre': 'Cable Instrumento Blindado Premium 6 Metros',
                'descripcion': 'Conectores dorados libres de ruido y malla trenzada.',
                'categoria': cat_objs['tecnologia-y-audio'],
                'marca': marca_objs['Boss'],
                'proveedor': prov_objs['Instrumentos del Pacífico Ltda.'],
                'precio': 15990,
                'stock': 70,
                'stock_minimo': 20,
            },
            # Producto sin solicitudes para Reporte 15
            {
                'sku': 'ACC-METRONOMO-01',
                'nombre': 'Metrónomo Digital Clip Compacto',
                'descripcion': 'Afinador y metrónomo portátil clip-on.',
                'categoria': cat_objs['tecnologia-y-audio'],
                'marca': marca_objs['Korg'],
                'proveedor': prov_objs['Distribuidora Global Sound S.A.'],
                'precio': 12900,
                'stock': 25,
                'stock_minimo': 5,
            },
        ]

        prods_created = []
        for p in productos_data:
            prod_obj, created = Producto.objects.update_or_create(sku=p['sku'], defaults=p)
            prods_created.append(prod_obj)
            if created and prod_obj.stock > 0:
                MovimientoStock.objects.create(
                    producto=prod_obj,
                    tipo='INGRESO',
                    cantidad=prod_obj.stock,
                    motivo='Inventario Inicial de Bodega Central'
                )

        # 6. Solicitudes de Sucursales y Detalles
        now = timezone.now()
        solicitudes_crear = [
            {
                'sucursal': suc_objs['Sucursal Santiago Centro'],
                'dias_atras': 2,
                'estado': 'PENDIENTE',
                'observacion': 'Requerimiento urgente de reposición de guitarras y micrófonos para fin de semana.',
                'detalles': [
                    ('GTR-FEND-STRAT-01', 3),
                    ('AUD-SHUR-SM58', 5),
                    ('MOB-SOP-GTR-01', 6),
                ]
            },
            {
                'sucursal': suc_objs['Sucursal Providencia'],
                'dias_atras': 5,
                'estado': 'APROBADA',
                'observacion': 'Pedido quincenal de teclados y audífonos de estudio.',
                'detalles': [
                    ('TEC-YAMA-P125', 2),
                    ('AUD-AT-M50X', 4),
                    ('AMP-BOSS-KAT50', 2),
                ]
            },
            {
                'sucursal': suc_objs['Sucursal Maipú'],
                'dias_atras': 10,
                'estado': 'DESPACHADA',
                'observacion': 'Reposición despachada en camión institucional.',
                'detalles': [
                    ('AUD-SHUR-SM58', 8),
                    ('MOB-ATRIL-PRO-01', 10),
                    ('ACC-CABLE-PRO-01', 15),
                ]
            },
            {
                'sucursal': suc_objs['Sucursal Viña del Mar'],
                'dias_atras': 14,
                'estado': 'DESPACHADA',
                'observacion': 'Despacho realizado conforme orden #SOL-450.',
                'detalles': [
                    ('GTR-FEND-STRAT-01', 2),
                    ('AMP-BOSS-KAT50', 3),
                    ('MOB-SOP-GTR-01', 8),
                ]
            },
            {
                'sucursal': suc_objs['Sucursal Concepción Centro'],
                'dias_atras': 20,
                'estado': 'PENDIENTE',
                'observacion': 'Pedido para temporada navideña y eventos de fin de año.',
                'detalles': [
                    ('TEC-KORG-MINILOG', 2),
                    ('AUD-AT-M50X', 6),
                    ('AUD-SHUR-SM58', 6),
                ]
            },
            {
                'sucursal': suc_objs['Sucursal Santiago Centro'],
                'dias_atras': 25,
                'estado': 'RECHAZADA',
                'observacion': 'Rechazado temporalmente por falta de cupo de transporte a la sucursal.',
                'detalles': [
                    ('GTR-GIBS-LES-01', 2),
                    ('AMP-MARS-DSL40', 1),
                ]
            },
            {
                'sucursal': suc_objs['Sucursal Providencia'],
                'dias_atras': 28,
                'estado': 'DESPACHADA',
                'observacion': 'Despacho de stock de soporte y cables.',
                'detalles': [
                    ('ACC-CABLE-PRO-01', 20),
                    ('MOB-ATRIL-PRO-01', 8),
                ]
            },
        ]

        for s_data in solicitudes_crear:
            sol, created = Solicitud.objects.get_or_create(
                sucursal=s_data['sucursal'],
                observacion=s_data['observacion'],
                defaults={
                    'estado': s_data['estado'],
                }
            )
            # Ajustar fecha en el pasado
            fecha_creacion = now - timedelta(days=s_data['dias_atras'])
            Solicitud.objects.filter(pk=sol.pk).update(fecha=fecha_creacion)

            for sku, cant in s_data['detalles']:
                try:
                    prod = Producto.objects.get(sku=sku)
                    DetalleSolicitud.objects.get_or_create(
                        solicitud=sol,
                        producto=prod,
                        defaults={'cantidad': cant}
                    )
                    # Si fue despachada, registrar movimiento de EGRESO en bodega
                    if s_data['estado'] == 'DESPACHADA':
                        mov, mov_created = MovimientoStock.objects.get_or_create(
                            solicitud=sol,
                            producto=prod,
                            tipo='EGRESO',
                            defaults={
                                'cantidad': cant,
                                'motivo': f'Despacho solicitud #{sol.pk} a {sol.sucursal.nombre}',
                            }
                        )
                        if mov_created:
                            MovimientoStock.objects.filter(pk=mov.pk).update(fecha=fecha_creacion)
                except Producto.DoesNotExist:
                    pass

        self.stdout.write(self.style.SUCCESS("¡Base de datos poblada con éxito con Proveedores, Sucursales, Productos, Solicitudes y Movimientos!"))
