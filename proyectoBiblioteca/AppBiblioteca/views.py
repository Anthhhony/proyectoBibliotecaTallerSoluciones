from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
<<<<<<< Updated upstream
from AppBiblioteca.models import Cliente, Libro, models, Prestamo, Categoria
=======
from AppBiblioteca.models import Cliente, Libro, models, Prestamo, Categoria, Usuario
from . import forms
from AppBiblioteca.forms import LibroForm
>>>>>>> Stashed changes

# Create your views here.

def vista(request):
    return render(request,"templatesApp/menu.html")

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

def mostrar_libros(request):
    libros = Libro.objects.all()
    categoria = Categoria.objects.all()
    return render(request, 'templatesApp/libros.html', {'libros':libros, 'categoria':categoria})

def agregar_libro(request):
    titulo = 'Agregar'
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            nombre_categoria = request.POST.get('nombre_categoria')
            categoria, creada = Categoria.objects.get_or_create(nombre=nombre_categoria)
            
            libro = form.save(commit=False)
            libro.save()
            libro.categorias.add(categoria)
            form.save_m2m()
            return redirect(mostrar_libros)
    else:
        form = LibroForm()
        categorias = Categoria.objects.all()
    return render(request, 'templatesApp/form_libro.html', {
        'form': form,
        'categorias':categorias,
        'titulo':titulo
    })

def editar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    titulo = 'Editar'
    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            return redirect(mostrar_libros)
    else:
        form = LibroForm(instance=libro)
    
    return render(request, 'templatesApp/form_libro.html', {'form': form, 'libro': libro, 'titulo':titulo})

def eliminar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        libro.delete()
        return redirect(mostrar_libros)
    
    return render(request, 'templatesApp/eliminar_confirmacion.html', {'libro': libro})


