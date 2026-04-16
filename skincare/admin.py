from django.contrib import admin
from .models import Usuario, Ingrediente, Producto, Rutina, AnalisisIA, PasoRutina

# Aquí registramos tus tablas para que aparezcan en el panel 😎
admin.site.register(Usuario)
admin.site.register(Ingrediente)
admin.site.register(Producto)
admin.site.register(Rutina)
admin.site.register(AnalisisIA)
admin.site.register(PasoRutina)