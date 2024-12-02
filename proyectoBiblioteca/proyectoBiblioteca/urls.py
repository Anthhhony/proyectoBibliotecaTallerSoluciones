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
        # path('editarLibro/<int:pk>', editar_libro, name='editar-libro'),
    # path('eliminarLibro/<int:pk>', eliminar_libro, name='eliminar-libro')
"""
from django.contrib import admin
from django.urls import path
from AppBiblioteca.views import vista, mostrar_editoriales, mostrar_autores, mostrar_categorias, agregar_categoria, eliminar_categoria, lista_prestamos, procesar_prestamo, prestamos_confirmados, finalizar_prestamo, eliminar_prestamo, mostrar_libros, agregar_libro, editar_libro, eliminar_libro, register, buscar_usuario, mostrar_clientes, agregar_cliente, editar_cliente, eliminar_cliente
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='registrar-usuario'),
    path('', buscar_usuario, name='buscar-usuario'),
    path('menu/', vista, name='menu-principal'),
    path('prestamo/', lista_prestamos, name='lista-prestamo'),
    path('procesarPrestamo/<int:libro_id>', procesar_prestamo, name='procesar-prestamo'),
    path('prestamosProcesados/', prestamos_confirmados, name='prestamos-confirmados'),
    path('finalizarPrestamo/<int:prestamo_id>', finalizar_prestamo, name='finalizar-prestamo'),
    path('eliminarPrestamo/<int:prestamo_id>', eliminar_prestamo, name='eliminar-prestamo'),
    path('libros/', mostrar_libros, name='mostrar-libros'),
    path('agregarLibro/', agregar_libro, name='agregar-libro'),
    path('editarLibro/<int:pk>', editar_libro, name='editar-libro'),
    path('eliminarLibro/<int:pk>', eliminar_libro, name='eliminar-libro'),
    path('clientes/', mostrar_clientes, name='mostrar-clientes'),
    path('agregarClientes/', agregar_cliente, name='agregar-cliente'),
    path('editarCliente/<int:pk>', editar_cliente, name='editar-cliente'),
    path('eliminarCliente/<int:pk>', eliminar_cliente, name='eliminar-cliente'),
     path('categorias/', mostrar_categorias, name='mostrar-categorias'),
    path('agregarCategoria/', agregar_categoria, name='agregar-categoria'),
    path('eliminarCategoria/<int:id>/', eliminar_categoria, name='eliminar-categoria'),
    path('editoriales/', mostrar_editoriales, name='mostrar-editoriales'),
    path('autores/', mostrar_autores, name='mostrar-autores'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
