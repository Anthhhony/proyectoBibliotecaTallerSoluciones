from django.db import models
from django.core import validators
from django.core.validators import RegexValidator, EmailValidator, MaxLengthValidator, MinLengthValidator, MaxValueValidator, MinValueValidator

# Create your models here.
class Usuario(models.Model):
    rut = models.CharField(
        max_length=12,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{1,8}-{0,9Kk}$', message='Rut incorrecto. Ejemplo: 12345678-9')]
    )
    contrasena = models.CharField(max_length=100)
    
    def __str__(self):
        return self.rut

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    
    
    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre =  models.CharField(max_length=50, validators=[MinValueValidator(3)])
    direccion = models.CharField(max_length=100, validators=[MinValueValidator(3)])
    telefono = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^(?:\+56|56)?9\d{8}$', message='Telefono incorrecto. Ejemplo: +56912345678')]
    )
    correo = models.EmailField(
        validators=[EmailValidator(message='Correo incorrecto.')]
    )
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
class Libro(models.Model):
    isbn = models.CharField(max_length=100, unique=True)
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=50)
    editorial = models.CharField(max_length=50)
    anio_publicacion = models.BigIntegerField()
    disponibilidad = models.BooleanField(default=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    categorias = models.ManyToManyField(Categoria, related_name='libros')
    
    def __str__(self):
        return self.titulo

class Prestamo(models.Model):
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField()
    estado = models.BooleanField(default=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"Prestamo - {self.cliente.nombre}"
    