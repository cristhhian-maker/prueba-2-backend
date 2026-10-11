from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from faker import Faker
import random

fake = Faker('es_CL')  # Datos en español/Chile


class Command(BaseCommand):
    help = (
        'Genera usuarios falsos de prueba usando Faker. '
        'Ejemplo: python manage.py seed_users --cantidad 100'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--cantidad',
            type=int,
            default=50,
            help='Número de usuarios a crear (default: 50)',
        )
        parser.add_argument(
            '--password',
            type=str,
            default='test1234',
            help='Contraseña común para todos los usuarios generados (default: test1234)',
        )
        parser.add_argument(
            '--staff',
            action='store_true',
            default=False,
            help='Si se incluye, algunos usuarios serán marcados como staff',
        )

    def handle(self, *args, **options):
        cantidad = options['cantidad']
        password = options['password']
        include_staff = options['staff']

        if cantidad < 1 or cantidad > 10_000:
            raise CommandError('La cantidad debe estar entre 1 y 10.000.')

        self.stdout.write(
            self.style.MIGRATE_HEADING(
                f'\nGenerando {cantidad} usuario(s) con Faker...\n'
            )
        )

        creados = 0
        omitidos = 0

        for i in range(cantidad):
            first_name = fake.first_name()
            last_name  = fake.last_name()

            # Genera username único basado en nombre + número aleatorio
            base_username = (
                f"{first_name.lower().replace(' ', '')}"
                f".{last_name.lower().replace(' ', '')}"
                f"{random.randint(1, 9999)}"
            )
            # Trunca a 150 chars (límite de Django)
            username = base_username[:150]

            # Omite si ya existe
            if User.objects.filter(username=username).exists():
                omitidos += 1
                continue

            is_staff = include_staff and (i % 10 == 0)  # 1 de cada 10 es staff

            User.objects.create_user(
                username=username,
                email=fake.email(),
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_staff=is_staff,
                is_active=True,
            )
            creados += 1

            # Muestra progreso cada 50 usuarios
            if creados % 50 == 0:
                self.stdout.write(f'  -> {creados} usuarios creados...')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'[OK] Usuarios creados : {creados}'))
        if omitidos:
            self.stdout.write(self.style.WARNING(f'[!] Omitidos (ya existian): {omitidos}'))
        self.stdout.write(
            self.style.SUCCESS(
                f'Contrasena comun para todos: {password}\n'
            )
        )
