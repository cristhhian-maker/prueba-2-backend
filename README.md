\# Sistema de Gestión de Bodega - Django Backend



Este proyecto consiste en una aplicación backend desarrollada en \*\*Django\*\* para el control, almacenamiento y administración automatizada de productos, categorías y movimientos de stock dentro de una bodega.



\---



\## 🛠️ Tecnologías y Configuración del Entorno

\* \*\*Framework principal:\*\* Django 5.x

\* \*\*Base de datos identificada:\*\* SQLite (`db.sqlite3`), configurada en el entorno de desarrollo a través de `config/settings.py`.

\* \*\*Generador de datos ficticios:\*\* Faker (para pruebas de carga de componentes).



\---



\## 📊 Modelamiento y Diagrama de Base de Datos

El diseño relacional se compone de entidades estructuradas mediante el ORM de Django:



1\. \*\*Categoria:\*\* Clasificación de los artículos (Ej: Herramientas, Maquinaria, EPP).

2\. \*\*Producto:\*\* Bienes almacenados con atributos de precio, stock actual y clave foránea (`ForeignKey`) vinculada a su categoría.

3\. \*\*Movimiento (Opcional según flujo):\*\* Registro transaccional de entradas y salidas de stock.



\### Estructura de Entidades

\* \*\*Tabla Categoria:\*\* `id` (PK) | `nombre` (Unique) | `descripcion`

\* \*\*Tabla Producto:\*\* `id` (PK) | `nombre` | `precio` | `stock` | `fecha\_creacion` | `categoria\_id` (FK -> Categoria)



\---



\## 🚀 Migraciones y Control de Versiones

Las migraciones permiten registrar, versionar y aplicar los cambios estructurales del modelo sobre la base de datos sin perder la integridad del historial.



Para sincronizar la estructura, ejecute en la consola:

```bash

python manage.py makemigrations

python manage.py migrate

```



\---



\## 🛡️ Django Admin y Operaciones CRUD

El panel administrativo estándar ha sido personalizado en `bodega/admin.py` para facilitar la gestión del ciclo de vida de los datos (\*\*C\*\*reate, \*\*R\*\*ead, \*\*U\*\*pdate, \*\*D\*\*elete):

\* \*\*Filtros avanzados:\*\* Segmentación lateral por categorías y rangos de fechas de creación.

\* \*\*Búsquedas indexadas:\*\* Barra de búsqueda por coincidencia de texto en nombres de productos y categorías relacionadas.

\* \*\*Edición en lista:\*\* Modificación veloz de stock y precios directamente desde la tabla general.



\---



\## 🧪 Generación de Datos de Prueba (Seeders)

La aplicación cuenta con mecanismos automatizados para poblar la base de datos con información ficticia masiva utilizando la librería `Faker`:



Para poblar las tablas mediante el comando nativo de Django, ejecute:

```bash

python manage.py seed\_data

```

O de manera alternativa, use el script independiente de la raíz:

```bash

python poblar.py

```



