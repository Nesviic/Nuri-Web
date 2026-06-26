# skincare/services.py
from .models import Ingrediente

class InciAnalyzer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(InciAnalyzer, cls).__new__(cls, *args, **kwargs)
            # Al crearse la única instancia, se inicializan los datos desde la BD
            cls._instance._load_restrictions_cache()
        return cls._instance

    def _load_restrictions_cache(self):
        """
        Consulta la base de datos a través del ORM una sola vez para almacenar 
        en memoria los ingredientes que no son seguros o que generan alertas.
        """
        # Guardamos en un conjunto (set) para búsquedas de alta velocidad O(1)
        self.ingredientes_criticos = set(
            Ingrediente.objects.filter(es_seguro=False).values_list('nombre', flat=True)
        )
        print("Caché del Singleton InciAnalyzer inicializado con datos de la BD.")

    def actualizar_cache(self):
        """
        Permite refrescar la memoria del Singleton si se añaden o modifican 
        ingredientes desde el panel de administración sin reiniciar el servidor.
        """
        self._load_restrictions_cache()

    def analizar_compatibilidad(self, lista_ingredientes_producto):
        """
        Compara los ingredientes de un producto contra las restricciones en memoria.
        """
        alertas_detectadas = [
            ingrediente for ingrediente in lista_ingredientes_producto 
            if ingrediente.lower() in (critico.lower() for critico in self.ingredientes_criticos)
        ]
        
        return {
            "es_compatible": len(alertas_detectadas) == 0,
            "alertas": alertas_detectadas
        }