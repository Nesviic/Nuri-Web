from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroUsuarioForm(UserCreationForm):
    # Creamos una lista desplegable para el tipo de piel
    TIPO_PIEL_CHOICES = [
        ('', 'Selecciona tu tipo de piel'),
        ('normal', 'Normal'),
        ('seca', 'Seca'),
        ('grasa', 'Grasa'),
        ('mixta', 'Mixta'),
        ('sensible', 'Sensible'),
    ]
    
    tipo_piel = forms.ChoiceField(
        choices=TIPO_PIEL_CHOICES, 
        required=False,
        # Ya no necesitamos las clases largas aquí porque registro.css hace el trabajo
        widget=forms.Select()
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        # Estos son los campos que le pediremos al usuario
        fields = ['username', 'email', 'tipo_piel']

    # --- AQUÍ ESTÁ LA MAGIA PARA LIMPIAR LOS TEXTOS ---
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 1. Hacemos que el email sea obligatorio (útil para tu base de datos)
        self.fields['email'].required = True
        
        # 2. Resumimos los textos de ayuda gigantes de Django
        self.fields['username'].help_text = "Solo letras, números y símbolos @/./+/-/_"
        
        # Django llama a la primera contraseña 'password1' por defecto
        if 'password1' in self.fields:
            self.fields['password1'].help_text = "Usa al menos 8 caracteres y evita contraseñas comunes."