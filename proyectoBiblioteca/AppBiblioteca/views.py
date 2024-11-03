from datetime import date
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from AppBiblioteca.models import Cliente, Libro, models, Prestamo, Categoria, Usuario
from . import forms
from django.contrib import messages
from django.urls import reverse

# Create your views here.

def login(request):
    return render(request, "templatesApp/inicio.html")

def vista(request):
    return render(request,"templatesApp/menu.html")

def buscar_usuario(request):
    if request.method == "POST":
        rut = request.POST.get('rut')
        usuario = Usuario.objects.filter(rut=rut)
        print(rut)
        
        if usuario:
            return render(request, "templatesApp/menu.html")
        
        else:
            messages.error(request, "El R.U.N ingresado no se encuentra registrado.")
            return redirect('buscar-usuario')

    return render(request, 'templatesApp/inicio.html')
        
def register(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        contrasena = request.POST.get('contrasena')

        # Verificar si el RUT ya existe en la base de datos
        if Usuario.objects.filter(rut=rut).exists():
            messages.error(request, "Este R.U.N ya está registrado.")
            return redirect('registrar-usuario')  # Redirige usando el nombre de la URL

        # Crear el nuevo usuario
        usuario = Usuario(rut=rut, contrasena=contrasena)
        usuario.save()
        messages.success(request, "Usuario registrado exitosamente.")
        
        # Redirigir a la página de inicio de sesión o donde prefieras
        return redirect('login')  # Redirige usando el nombre de la URL

    return render(request, 'templatesApp/registro_inicio.html')

def lista_prestamos(request):
    libros_disponibles = Libro.objects.filter(disponibilidad=True)
    return render(request, 'templatesApp/prestamo.html', {'libros':libros_disponibles})

def procesar_prestamo(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    clientes = Cliente.objects.all()
    categorias = Categoria.objects.all()
    
    if request.method=='POST':
        cliente_id = request.POST['cliente']
        categoria_id = request.POST['categoria']
        fecha_prestamo = request.POST['fecha_prestamo']
        fecha_devolucion = request.POST['fecha_devolucion']
        
        cliente = get_object_or_404(Cliente, id=cliente_id)
        categoria = get_object_or_404(Categoria, id=categoria_id)
        
        prestamo = Prestamo(
            cliente=cliente,
            libro=libro,
            categoria=categoria,
            fecha_prestamo=fecha_prestamo,
            fecha_devolucion=fecha_devolucion
        )
        prestamo.save()
        return redirect(prestamos_confirmados)
    return render(request, 'templatesApp/procesar_prestamo.html', {
        'libro':libro,
        'clientes':clientes,
        'categorias':categorias,
    })

def prestamos_confirmados(request):
    prestamos = Prestamo.objects.all()
    return render(request, 'templatesApp/prestamos_confirmados.html', {'prestamos':prestamos})

def finalizar_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    if request.method == 'POST':
        prestamo.estado = True
        prestamo.save()
        return redirect(prestamos_confirmados)

def eliminar_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    if request.method == 'POST':
        prestamo.delete()
        return redirect(prestamos_confirmados)

    


