from datetime import date
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.core.mail import send_mail
from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from AppBiblioteca.models import Cliente, Libro, models, Prestamo, Categoria, Usuario
from AppBiblioteca.forms import ClienteForm, LibroForm
from . import forms
from django.db.models import Q, Count
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

def login(request):
    return render(request, "templatesApp/inicio.html")

def vista(request):
    return render(request,"templatesApp/menu.html")

def buscar_usuario(request):
    if request.method == "POST":
        rut = request.POST.get('rut')
        contrasena = request.POST.get('contrasena')
        
        usuario = Usuario.objects.filter(rut=rut).first()
        
        if usuario and check_password(contrasena, usuario.contrasena):
            return render(request, "templatesApp/menu.html")
        else:
            messages.error(request, "R.U.N o contraseña incorrecta.")
            return redirect('buscar-usuario')
            
    return render(request, "templatesApp/inicio.html")

        
def register(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        nombre = request.POST.get('nombre')  # Capturar el nombre
        correo = request.POST.get('correo')  # Capturar el correo
        telefono = request.POST.get('telefono')  # Capturar el teléfono
        contrasena = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Validar contraseñas
        if contrasena != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('registrar-usuario')

        # Verificar si el RUT ya existe
        if Usuario.objects.filter(rut=rut).exists():
            messages.error(request, "Este R.U.N ya está registrado.")
            return redirect('registrar-usuario')

        # Verificar si el correo ya está en uso
        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, "Este correo ya está registrado.")
            return redirect('registrar-usuario')

        # Validar que el teléfono contenga solo números y tenga el largo correcto
        if not telefono.isdigit() or len(telefono) not in [9, 10]:
            messages.error(request, "El número de teléfono debe contener 9 o 10 dígitos.")
            return redirect('registrar-usuario')

        # Crear el nuevo usuario
        usuario = Usuario(
            rut=rut,
            nombre=nombre,
            correo=correo,
            telefono=telefono,
            contrasena=make_password(contrasena)  # Encriptar la contraseña
        )
        usuario.save()
        messages.success(request, "Usuario registrado exitosamente.")
        return redirect('buscar-usuario')

    return render(request, 'templatesApp/registro_inicio.html')


def lista_prestamos(request):
    libros_disponibles = Libro.objects.filter(disponibilidad=True)
    query = request.GET.get('buscar', '').strip()  # 'buscar' es el nombre del input en el template

    if query:  # Si hay una búsqueda, filtrar por nombre o ISBN
        libros_disponibles = libros_disponibles.filter(
            Q(titulo__icontains=query) | Q(isbn__icontains=query)
        )

    return render(request, 'templatesApp/prestamo.html', {'libros': libros_disponibles})

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
        libro.disponibilidad=False
        libro.save()
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
        
        libro = prestamo.libro
        libro.disponibilidad = True
        libro.save()

        return redirect(prestamos_confirmados)

def eliminar_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    if request.method == 'POST':
        prestamo.delete()
        return redirect(prestamos_confirmados)
    return render(request, "templatesApp/eliminar_confirmacion.html", {"prestamo":prestamo})
    
def mostrar_libros(request):
    query = request.GET.get('buscar', '')
    if query:
        libros = Libro.objects.filter(
            Q(titulo__icontains=query) | Q(isbn__icontains=query)
        )
    else:
        libros = Libro.objects.all()
    categoria = Categoria.objects.all()
    return render(request, 'templatesApp/libros.html', {'libros':libros, 'categoria':categoria})

def agregar_libro(request):
    titulo = 'Agregar'
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            libro = form.save(commit=False)
            libro.save()
            form.save_m2m()
            return redirect(mostrar_libros)
    else:
        form = LibroForm()

    return render(request, 'templatesApp/form_libro.html', {
        'form': form,
        'titulo':titulo
    })

def editar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    titulo = 'Editar'
    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            libro = form.save(commit=False)  # Guarda el libro sin aplicar las relaciones ManyToMany aún
            libro.save()
            # Actualizar las categorías
            categorias = form.cleaned_data.get('categorias')  # Obtener las categorías seleccionadas
            libro.categorias.set(categorias)  # Actualizar las categorías relacionadas
            return redirect('mostrar-libros')
    else:
        form = LibroForm(instance=libro)
    
    return render(request, 'templatesApp/form_libro.html', {'form': form, 'libro': libro, 'titulo': titulo})

def eliminar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        libro.delete()
        return redirect(mostrar_libros)
    
    return render(request, 'templatesApp/eliminar_confirmacion.html', {'libro': libro})



def mostrar_clientes(request):
    query = request.GET.get('buscarCliente', '').strip()
    if query:
        # Filtrar clientes por nombre o RUT
        cliente = Cliente.objects.filter(
            Q(nombre__icontains=query) | Q(usuario__rut__icontains=query)
        )
    else:
        # Mostrar todos los clientes si no hay búsqueda
        cliente = Cliente.objects.all()
    
    return render(request, 'templatesApp/clientes.html', {'cliente': cliente})



def agregar_cliente(request):
    titulo = 'Agregar'
    form = ClienteForm()
    
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.save()
            return redirect(mostrar_clientes)
        
    return render(request, 'templatesApp/form_cliente.html', {
        'form':form,
        'titulo':titulo
    })

def editar_cliente(request, pk):
    titulo = 'Editar'
    cliente = Cliente.objects.get(id=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect(mostrar_clientes)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'templatesApp/form_cliente.html', {'form':form,'cliente':cliente, 'titulo':titulo})

def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect(mostrar_clientes)
    return render(request, 'templatesApp/eliminar_confirmacion.html', {'cliente':cliente})


def mostrar_categorias(request):
    categorias = Categoria.objects.annotate(cantidad_libros=Count('libros'))
    return render(request, 'templatesApp/categorias.html', {'categorias': categorias})

def agregar_categoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        if nombre:  # Validación básica
            Categoria.objects.create(nombre=nombre)
            return redirect('mostrar-categorias')
    return render(request, 'templatesApp/agregar_categoria.html')

def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('mostrar-categorias')
    return render(request, 'templatesApp/eliminar_confirmacion.html', {'categoria':categoria})

def mostrar_editoriales(request):
    query = request.GET.get('q', '')  # Obtener el término de búsqueda
    editoriales = (
        Libro.objects.filter(editorial__icontains=query) if query else Libro.objects.all()
    ).values('editorial').annotate(cantidad=Count('id')).order_by('editorial')
    
    return render(request, 'templatesApp/editoriales.html', {
        'editoriales': editoriales,
        'query': query,
    })

def mostrar_autores(request):
    query = request.GET.get('q', '')  # Obtener el término de búsqueda
    autores = (
        Libro.objects.filter(autor__icontains=query) if query else Libro.objects.all()
    ).values('autor').annotate(cantidad=Count('id')).order_by('autor')
    
    return render(request, 'templatesApp/autores.html', {
        'autores': autores,
        'query': query,
    })



