from django.contrib import admin
from AppBiblioteca.models import Libro, Categoria, Cliente, Prestamo, Usuario

# Register your models here.
@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('isbn','titulo', 'autor', 'editorial', 'anio_publicacion', 'disponibilidad')
    list_filter = ('disponibilidad',)
    search_fields = ('titulo', 'isbn')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono', 'correo', 'usuario')
    search_fields = ('nombre', 'correo')
    
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('rut', 'contrasena')
    search_fields = ('rut',)

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('fecha_prestamo', 'fecha_devolucion', 'estado', 'cliente', 'libro', 'categoria', 'usuario')
    search_fields = ('cliente', 'fecha_prestamo', 'usuario')