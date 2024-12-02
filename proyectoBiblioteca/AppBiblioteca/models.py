from django.db import models
from django.core import validators
from django.core.validators import RegexValidator, EmailValidator, MaxLengthValidator, MinLengthValidator, MaxValueValidator, MinValueValidator

# Create your models here.
    
class Usuario(models.Model):

    nombre = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
                message="El nombre solo puede contener letras y espacios."
            )
        ]
    )

    rut = models.CharField(
        max_length=12,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{1,2}\.\d{3}\.\d{3}-[0-9kK]$',
                message="El RUT debe tener el formato chileno: 12.345.678-9 o 1.234.567-K."
            )
        ]
    )

    contrasena = models.CharField(
        max_length=128,
        validators=[
            MinLengthValidator(8, message="La contraseña debe tener al menos 8 caracteres."),
            RegexValidator(
                regex=r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
                message="La contraseña debe incluir al menos una letra, un número y un símbolo especial."
            )
        ]
    )

    correo = models.EmailField(
        unique=True,
        null=True,
        blank=True,
        validators=[EmailValidator(message="Debe ser un correo válido.")]
    )

    telefono = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{8,15}$',
                message="El número de teléfono debe tener entre 8 y 15 dígitos, con o sin prefijo '+' al inicio."
            )
        ]
    )

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    
    
    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre =  models.CharField(max_length=50, validators=[MinLengthValidator(3)])
    direccion = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
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
    