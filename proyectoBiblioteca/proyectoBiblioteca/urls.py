"""proyectoBiblioteca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from AppBiblioteca.views import vista, lista_prestamos, procesar_prestamo, prestamos_confirmados, finalizar_prestamo, eliminar_prestamo, login, registrar_usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gggg', login, name='login'),
    path('registroInicio/', registrar_usuario, name='registrar-usuario'),
    path('', vista, name='menu-principal'),
    path('prestamo/', lista_prestamos, name='lista-prestamo'),
    path('procesarPrestamo/<int:libro_id>', procesar_prestamo, name='procesar-prestamo'),
    path('prestamosProcesados/', prestamos_confirmados, name='prestamos-confirmados'),
    path('finalizarPrestamo/<int:prestamo_id>', finalizar_prestamo, name='finalizar-prestamo'),
    path('eliminarPrestamo/<int:prestamo_id>', eliminar_prestamo, name='eliminar-prestamo')
]
