from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from AppBiblioteca.models import Cliente, Libro, models, Prestamo, Categoria, Usuario
from . import forms

# Create your views here.

def login(request):
    return render(request, "templatesApp/inicio.html")

def vista(request):
    return render(request,"templatesApp/menu.html")

def buscar_usuario(request, rut):
    usuario = Usuario.objects.filter(rut=rut).first()
    if request.method == "POST":
        if usuario:
            data = {"usuario":usuario}
            return render(request, 'templatesApp/menu.html', data)
        
        else:
            return None
        
def registrar_usuario(request):
    form = forms.formularioLogin()
    if request.method=="POST":
        form = forms.formularioLogin(request.POST)
        if form.is_valid():
            db = Usuario(
                rut = form.cleaned_data["rut"],
                contrasena = form.cleaned_data["contraseña"],
            )
            db.save()
            return render(request, "templatesApp/inicio.html")
    return render(request, "templatesApp/registro_inicio.html")

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

    


