import json
from django.core.management.base import BaseCommand
from skincare.models import Producto, Ingrediente  # Ajustá a tus modelos

class Command(BaseCommand):
    help = 'Carga productos desde un JSON sin duplicar ingredientes'

    def handle(self, *args, **options):
        # Aquí pegás la variable que te pasé
        data = [
            {
                "id": 1,
                "name": "Hyalu B5 Serum",
                "brand": "La Roche-Posay",
                "main_ingredients": ["Ácido hialurónico", "Pantenol"]
            },
            # ... el resto de los productos ...
        ]

        for item in data:
            # Creamos el producto (o usamos update_or_create para no duplicar productos)
            producto, created = Producto.objects.get_or_create(
                nombre=item['name'],
                marca=item['brand'],
                defaults={
                    'categoria': item['category'],
                    'descripcion': item['characteristics']
                }
            )

            # Lógica para los ingredientes (Many-to-Many)
            for ing_name in item['main_ingredients']:
                # get_or_create es la clave: si ya existe (como en tu admin), lo usa; si no, lo crea.
                ingrediente, _ = Ingrediente.objects.get_or_create(nombre=ing_name)
                producto.ingredientes.add(ingrediente)

        self.stdout.write(self.style.SUCCESS('¡Base de datos de Nuri actualizada con éxito!'))