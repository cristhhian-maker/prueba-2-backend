from django.core.management.base import BaseCommand
from bodega.models import Categoria, Marca, Producto, MovimientoStock

class Command(BaseCommand):
    help = 'Puebla la base de datos con categorías, marcas y productos musicales de prueba para MusicPro'

    def handle(self, *args, **options):
        self.stdout.write("Insertando datos iniciales...")

        # Categorías
        cats = [
            {'nombre': 'Guitarras y Bajos', 'slug': 'guitarras-y-bajos', 'descripcion': 'Guitarras eléctricas, acústicas, electroacústicas y bajos'},
            {'nombre': 'Teclados y Sintetizadores', 'slug': 'teclados-y-sintetizadores', 'descripcion': 'Pianos digitales, controladores MIDI y sintetizadores'},
            {'nombre': 'Baterías y Percución', 'slug': 'baterias-y-percusion', 'descripcion': 'Baterías acústicas, electrónicas, platillos y accesorios'},
            {'nombre': 'Audio Pro y Micrófonos', 'slug': 'audio-pro-y-microfonos', 'descripcion': 'Micrófonos de estudio, monitores, consolas y auriculares'},
            {'nombre': 'Amplificadores y Efectos', 'slug': 'amplificadores-y-efectos', 'descripcion': 'Cabezales, cajas, pedales de efectos y multi-efectos'},
        ]
        
        cat_objs = {}
        for c in cats:
            obj, _ = Categoria.objects.get_or_create(slug=c['slug'], defaults=c)
            cat_objs[c['slug']] = obj

        # Marcas
        marcas = [
            {'nombre': 'Fender', 'pais_origen': 'EE.UU.'},
            {'nombre': 'Gibson', 'pais_origen': 'EE.UU.'},
            {'nombre': 'Yamaha', 'pais_origen': 'Japón'},
            {'nombre': 'Roland', 'pais_origen': 'Japón'},
            {'nombre': 'Shure', 'pais_origen': 'EE.UU.'},
            {'nombre': 'Marshall', 'pais_origen': 'Reino Unido'},
            {'nombre': 'Boss', 'pais_origen': 'Japón'},
            {'nombre': 'Pearl', 'pais_origen': 'Japón'},
        ]

        marca_objs = {}
        for m in marcas:
            obj, _ = Marca.objects.get_or_create(nombre=m['nombre'], defaults=m)
            marca_objs[m['nombre']] = obj

        # Productos
        productos = [
            {
                'sku': 'GTR-FEND-STRAT-01',
                'nombre': 'Fender Player Stratocaster Maple MN 3TS',
                'descripcion': 'Guitarra eléctrica icónica Fender con pastillas Player Series Single-Coil.',
                'categoria': cat_objs['guitarras-y-bajos'],
                'marca': marca_objs['Fender'],
                'precio': 899000,
                'stock': 12,
                'stock_minimo': 3,
            },
            {
                'sku': 'GTR-GIBS-LES-01',
                'nombre': 'Gibson Les Paul Standard 50s Heritage Cherry',
                'descripcion': 'Guitarra de cuerpo macizo de caoba con tapa de arce figurado AA.',
                'categoria': cat_objs['guitarras-y-bajos'],
                'marca': marca_objs['Gibson'],
                'precio': 2490000,
                'stock': 2,
                'stock_minimo': 2,
            },
            {
                'sku': 'TEC-YAMA-P125',
                'nombre': 'Yamaha P-125B Piano Digital 88 Teclas',
                'descripcion': 'Piano digital compacto con motor de sonido Pure CF y contrapeso Graded Hammer Standard.',
                'categoria': cat_objs['teclados-y-sintetizadores'],
                'marca': marca_objs['Yamaha'],
                'precio': 649000,
                'stock': 8,
                'stock_minimo': 4,
            },
            {
                'sku': 'TEC-ROLA-JUNO',
                'nombre': 'Roland JUNO-DS61 Sintetizador',
                'descripcion': 'Sintetizador portátil de 61 teclas con voces profesionales y reproducción de muestras.',
                'categoria': cat_objs['teclados-y-sintetizadores'],
                'marca': marca_objs['Roland'],
                'precio': 789000,
                'stock': 1,
                'stock_minimo': 3,
            },
            {
                'sku': 'BAT-PEAR-ROAD-01',
                'nombre': 'Pearl Roadshow RS525W/C Batería Acústica 5 Piezas',
                'descripcion': 'Set completo de batería acústica incluye fierros, platillos y sillín.',
                'categoria': cat_objs['baterias-y-percusion'],
                'marca': marca_objs['Pearl'],
                'precio': 599000,
                'stock': 0,
                'stock_minimo': 2,
            },
            {
                'sku': 'AUD-SHUR-SM58',
                'nombre': 'Shure SM58-LC Micrófono Dinámico Vocal',
                'descripcion': 'El estándar de la industria para presentaciones vocales en vivo.',
                'categoria': cat_objs['audio-pro-y-microfonos'],
                'marca': marca_objs['Shure'],
                'precio': 119000,
                'stock': 25,
                'stock_minimo': 5,
            },
            {
                'sku': 'AMP-MARS-DSL40',
                'nombre': 'Marshall DSL40CR Combo Valvular 40W',
                'descripcion': 'Amplificador combo de tubos 1x12 de celestions V-Type con loop de efectos.',
                'categoria': cat_objs['amplificadores-y-efectos'],
                'marca': marca_objs['Marshall'],
                'precio': 849000,
                'stock': 3,
                'stock_minimo': 2,
            },
            {
                'sku': 'AMP-BOSS-KAT50',
                'nombre': 'Boss Katana-50 MkII Amplificador para Guitarra',
                'descripcion': 'Combo de 50 vatios con altavoz custom de 12 pulgadas y 5 caracteres de amplificador.',
                'categoria': cat_objs['amplificadores-y-efectos'],
                'marca': marca_objs['Boss'],
                'precio': 299000,
                'stock': 15,
                'stock_minimo': 4,
            },
        ]

        for p in productos:
            prod_obj, created = Producto.objects.get_or_create(sku=p['sku'], defaults=p)
            if created and prod_obj.stock > 0:
                MovimientoStock.objects.create(
                    producto=prod_obj,
                    tipo='INGRESO',
                    cantidad=prod_obj.stock,
                    motivo='Carga Inicial de Inventario'
                )

        self.stdout.write(self.style.SUCCESS("¡Datos iniciales cargados con éxito!"))
