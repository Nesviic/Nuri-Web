from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import RegistroUsuarioForm
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Ingrediente  
from django.contrib.auth.decorators import login_required
from .models import Rutina
from .models import Rutina, PasoRutina, Producto

def inicio(request):
    return render(request, 'index.html')

def analisis(request):
    return render(request, 'analisis.html')

# Este decorador patea a los intrusos hacia la página de login
@login_required(login_url='/login/')
def rutina(request):
    mi_rutina, created = Rutina.objects.get_or_create(
        usuario=request.user,
        defaults={'nombre_rutina': f'Rutina de {request.user.username}'}
    )
    
    pasos_am = mi_rutina.pasos.filter(momento='AM').order_by('orden')
    pasos_pm = mi_rutina.pasos.filter(momento='PM').order_by('orden')
    
    # NUEVO: Traemos todos los productos de la base de datos para mostrarlos en el buscador
    productos_disponibles = Producto.objects.all()
    
    return render(request, 'rutina.html', {
        'rutina': mi_rutina,
        'pasos_am': pasos_am,
        'pasos_pm': pasos_pm,
        'productos_disponibles': productos_disponibles # Lo enviamos a la pantalla
    })

def explorar(request):
    query = request.GET.get('q', '')
    lista_ingredientes = Ingrediente.objects.all().order_by('nombre') 
    
    if query:
        lista_ingredientes = lista_ingredientes.filter(
            Q(nombre__icontains=query) | Q(beneficio_principal__icontains=query)
        )

    paginator = Paginator(lista_ingredientes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    contexto = {
        'page_obj': page_obj, 
        'ingredientes': page_obj,  # <--- AGREGAMOS ESTA LÍNEA MÁGICA
        'query': query,
    }
    
    if request.headers.get('HX-Request'):
        return render(request, 'parcial_ingredientes.html', contexto)
    
    return render(request, 'explorar.html', contexto)

def registro(request):
    # Si el usuario apretó el botón de "Enviar" (POST)
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save() # Guarda al usuario en la base de datos de forma segura
            login(request, user) # Lo "loguea" automáticamente sin pedirle que vuelva a poner sus datos
            return redirect('inicio') # Lo mandamos a la página principal
    else:
        # Si recién entra a la página, le mostramos el formulario vacío (GET)
        form = RegistroUsuarioForm()
    
    return render(request, 'registro.html', {'form': form})

def detalle_ingrediente(request, id):
    # 1. Buscamos el ingrediente
    ingrediente = get_object_or_404(Ingrediente, id=id)
    
    # 2. Usamos tu related_name ('productos') para traer todos los limpiadores/serums mágicamente
    productos_relacionados = ingrediente.productos.all()
    
    # 3. Enviamos ambas cosas a la pantalla
    return render(request, 'detalle_ingrediente.html', {
        'ingrediente': ingrediente,
        'productos': productos_relacionados
    })

@login_required(login_url='/login/')
def agregar_paso(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        momento = request.POST.get('momento')
        
        mi_rutina, created = Rutina.objects.get_or_create(
            usuario=request.user,
            defaults={'nombre_rutina': f'Rutina de {request.user.username}'}
        )
        
        producto = get_object_or_404(Producto, id=producto_id)
        
        # EL ALGORITMO DE ORDENAMIENTO (De texturas más ligeras a más densas)
        # Basado en las reglas dermatológicas de Nuri
        prioridades = {
            'limpiador': 10,
            'mascarilla': 20, # Se enjuaga o va después de limpieza
            'tonico': 30,
            'escencia': 40,
            'serum': 50,
            'tratamiento': 60,
            'hidratante': 70, # Cremas
            'protector': 80,  # Siempre al final (AM)
            'otro': 99
        }
        
        # Le preguntamos al producto qué tipo es, y buscamos su número mágico. 
        # Si no lo encuentra, le da 99 para mandarlo al final.
        peso_orden = prioridades.get(producto.tipo_producto, 99)
        
        # Guardamos en la base de datos con ese "peso" específico
        PasoRutina.objects.create(
            rutina=mi_rutina,
            producto=producto,
            momento=momento,
            orden=peso_orden # Ahora el orden no es 1,2,3, sino 10, 50, 80...
        )
        
        return redirect('rutina')
        
    return redirect('rutina')

@login_required(login_url='/login/')
def eliminar_paso(request, paso_id):
    # Buscamos el paso específico
    paso = get_object_or_404(PasoRutina, id=paso_id)
    
    # Seguridad: Verificamos que el paso pertenezca a la rutina del usuario actual
    if paso.rutina.usuario == request.user:
        paso.delete()
        
    return redirect('rutina')

@login_required(login_url='/login/')
def actualizar_diagnostico(request):
    if request.method == 'POST':
        # Capturamos lo que el usuario seleccionó/escribió en el modal
        nuevo_tipo_piel = request.POST.get('tipo_piel')
        nuevas_preocupaciones = request.POST.get('preocupaciones')
        
        # Actualizamos al usuario actual
        user = request.user
        if nuevo_tipo_piel:
            user.tipo_piel = nuevo_tipo_piel
        if nuevas_preocupaciones:
            user.preocupaciones = nuevas_preocupaciones
            
        user.save()
        messages.success(request, '¡Diagnóstico actualizado con éxito!')
        
    return redirect('rutina')