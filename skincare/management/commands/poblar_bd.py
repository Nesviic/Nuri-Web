import json
import os
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils.text import slugify
from skincare.models import Producto, Ingrediente

class Command(BaseCommand):
    help = 'Carga masiva de productos e ingredientes con descarga de imágenes desde datos_nuri.json'

    def handle(self, *args, **kwargs):
        # 1. Buscamos el archivo JSON en la carpeta principal
        ruta_archivo = 'datos_nuri.json'
        
        if not os.path.exists(ruta_archivo):
            self.stdout.write(self.style.ERROR(f'No se encontró el archivo {ruta_archivo}'))
            return

        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)

        productos_creados = 0
        ingredientes_creados = 0
        imagenes_descargadas = 0

        # 2. Recorremos cada producto en el JSON
        for item in datos:
            # Creamos el producto
            producto, prod_creado = Producto.objects.get_or_create(
                nombre=item['nombre'],
                marca=item['marca'],
                defaults={'tipo_producto': item['tipo_producto']}
            )
            
            if prod_creado:
                productos_creados += 1

            # -------------------------------------------------------------------
            # LA NUEVA MAGIA: Descarga automática de imágenes
            # -------------------------------------------------------------------
            url_foto = item.get('url_imagen')
            
            # Si el JSON tiene URL y el producto aún no tiene imagen guardada
            if url_foto and not producto.imagen:
                try:
                    self.stdout.write(f"Descargando imagen para: {producto.nombre}...")
                    # Hacemos la petición a la URL (con un tiempo límite de 10 seg)
                    respuesta = requests.get(url_foto, timeout=10)
                    
                    if respuesta.status_code == 200:
                        # Creamos un nombre de archivo limpio (ej: cerave_limpiador_control.jpg)
                        nombre_archivo = f"{slugify(producto.marca)}_{slugify(producto.nombre)}.jpg"
                        
                        # Guardamos el archivo binario en el modelo
                        producto.imagen.save(nombre_archivo, ContentFile(respuesta.content), save=True)
                        imagenes_descargadas += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"⚠️ No se pudo descargar la imagen de {producto.nombre}: {e}"))
            # -------------------------------------------------------------------

            # 3. Recorremos los ingredientes de ese producto
            for ing_data in item['ingredientes']:
                ingrediente, ing_creado = Ingrediente.objects.get_or_create(
                    nombre=ing_data['nombre'],
                    defaults={
                        'beneficio_principal': ing_data['beneficio_principal'],
                        'categoria_principal': ing_data['categoria_principal']
                    }
                )
                
                if ing_creado:
                    ingredientes_creados += 1

                # Conectamos el ingrediente al producto
                producto.ingredientes.add(ingrediente)

        # Mensaje final de resumen
        self.stdout.write(self.style.SUCCESS(
            f'¡Éxito! Se procesaron {productos_creados} productos nuevos, {ingredientes_creados} ingredientes nuevos y se descargaron {imagenes_descargadas} imágenes.'
        ))