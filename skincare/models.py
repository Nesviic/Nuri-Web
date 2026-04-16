from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Heredamos de AbstractUser para cumplir con las reglas de Seguridad
class Usuario(AbstractUser):
    tipo_piel = models.CharField(max_length=45, blank=True, null=True)
    
    # --- NUEVOS CAMPOS PARA EL DASHBOARD ---
    preocupaciones = models.CharField(max_length=200, blank=True, null=True)
    hidratacion_actual = models.IntegerField(default=84) # 84% como en tu foto
    racha_dias = models.IntegerField(default=12) # 12 días como en tu foto

    def __str__(self):
        return self.username

# 2. Entidades Principales
class Ingrediente(models.Model):
    CATEGORIAS = [
        ('hidratante', 'Hidratante'),
        ('exfoliante', 'Exfoliante'),
        ('antioxidante', 'Antioxidante'),
        ('calmante', 'Calmante'),
        ('seborregulador', 'Control de Sebo'),
        ('otro', 'Otro'),
    ]
    
    nombre = models.CharField(max_length=100)
    beneficio_principal = models.CharField(max_length=200)
    categoria_principal = models.CharField(max_length=20, choices=CATEGORIAS, default='otro')

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    TIPOS_PRODUCTO = [
        ('limpiador', 'Limpiador'),
        ('tonico', 'Tónico'),
        ('escencia', 'Escencia'),
        ('serum', 'Serum'),
        ('hidratante', 'Hidratante'),
        ('protector', 'Protector Solar'),
        ('mascarilla', 'Mascarilla'),
        ('tratamiento', 'Tratamiento Específico'),
        ('otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    tipo_producto = models.CharField(max_length=20, choices=TIPOS_PRODUCTO, default='otro')
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    ingredientes = models.ManyToManyField(Ingrediente, related_name='productos')

    def __str__(self):
        return f"{self.marca} - {self.nombre}"

# 3. Entidades Transaccionales
class Rutina(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='rutinas')
    nombre_rutina = models.CharField(max_length=100) 
    # Mantenemos este campo para no romper tu base de datos vieja
    productos = models.ManyToManyField(Producto, related_name='rutinas', blank=True)

    def __str__(self):
        return f"{self.nombre_rutina} de {self.usuario.username}"

# --- NUEVA TABLA: PASOS AM Y PM ---
class PasoRutina(models.Model):
    MOMENTOS = [
        ('AM', 'Mañana (AM)'),
        ('PM', 'Noche (PM)')
    ]
    
    # Se conecta a la rutina y al producto
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE, related_name='pasos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    
    momento = models.CharField(max_length=2, choices=MOMENTOS, default='AM')
    orden = models.PositiveIntegerField(default=1) # Paso 1, Paso 2, etc.

    class Meta:
        ordering = ['momento', 'orden'] # Ordena automáticamente por AM/PM y luego por número

    def __str__(self):
        return f"{self.momento} - Paso {self.orden}: {self.producto.nombre}"

class AnalisisIA(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True) 
    nuri_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Análisis de {self.producto.nombre} para {self.usuario.username}"