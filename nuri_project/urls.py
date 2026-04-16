"""
URL configuration for nuri_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from skincare import views  
from django.contrib.auth.views import LoginView, LogoutView

# Importaciones necesarias para servir imágenes
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('analisis/', views.analisis, name='analisis'),
    path('rutina/', views.rutina, name='rutina'),
    path('rutina/agregar/', views.agregar_paso, name='agregar_paso'),
    path('explorar/', views.explorar, name='explorar'),
    path('ingrediente/<int:id>/', views.detalle_ingrediente, name='detalle_ingrediente'),
    path('registro/', views.registro, name='registro'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),
    path('rutina/eliminar/<int:paso_id>/', views.eliminar_paso, name='eliminar_paso'),
    path('rutina/diagnostico/', views.actualizar_diagnostico, name='actualizar_diagnostico'),
]

# Configuración para poder ver las imágenes multimedia en desarrollo local
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)