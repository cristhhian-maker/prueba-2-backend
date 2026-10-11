import os
import django
import random

# Configuración automática para tu proyecto 'config'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Importamos los modelos de tu app 'bodega'
# (Asegúrate de que tus modelos en bodega/models.py se llamen Categoria y Producto, 
# o cambia estos nombres por los tuyos)
from bodega.models import Categoria, Producto
from faker import Faker

fake = Faker(['es_ES']) # Datos en español

def generar_datos(n=20):
    print("Generando datos de prueba para la bodega...")
    
    # Crear categorías base
    categorias_nombres = ['Herramientas', 'Materiales', 'EPP', 'Maquinaria', 'Repuestos']
    categorias_objetos = []
    
    for cat in categorias_nombres:
        categoria, created = Categoria.objects.get_or_create(
            nombre=cat,
            defaults={'descripcion': fake.sentence()}
        )
        categorias_objetos.append(categoria)

    # Crear productos de prueba
    for _ in range(n):
        Producto.objects.create(
            categoria=random.choice(categorias_objetos),
            nombre=fake.word().capitalize() + " " + fake.word(),
            precio=round(random.uniform(1000.0, 50000.0), 2), # Precios adaptados
            stock=random.randint(5, 200)
        )
    
    print(f"¡Éxito! Se insertaron {n} artículos de prueba en la base de datos.")

if __name__ == '__main__':
    generar_datos(25)
