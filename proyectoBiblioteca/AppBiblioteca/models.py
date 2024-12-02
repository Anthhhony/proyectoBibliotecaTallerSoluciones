from django.db import models
from django.core import validators
from django.core.validators import RegexValidator, EmailValidator, MaxLengthValidator, MinLengthValidator, MaxValueValidator, MinValueValidator

# Create your models here.
    
class Usuario(models.Model):
    """
    Representa a un usuario en el sistema con sus datos básicos y credenciales.

    Attributes:
        nombre (CharField): Nombre del usuario, puede contener letras y espacios.
        rut (CharField): RUT del usuario en formato chileno, debe ser único.
        contrasena (CharField): Contraseña del usuario con validaciones específicas.
        correo (EmailField): Correo electrónico único del usuario.
        telefono (CharField): Número de teléfono del usuario con formato válido.
    """
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
        blank=True
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
        """
        Devuelve una representación en cadena del modelo.

        Returns:
            str: Nombre del usuario.
        """
        return self.nombre


class Categoria(models.Model):
    """
    Representa una categoría asociada a libros.

    Attributes:
        nombre (CharField): Nombre de la categoría, debe tener al menos 3 caracteres.
    """
    nombre = models.CharField(max_length=100, validators=[MinLengthValidator(3)])

    def __str__(self):
        """
        Devuelve una representación en cadena del modelo.

        Returns:
            str: Nombre de la categoría.
        """
        return self.nombre


class Cliente(models.Model):
    """
    Representa un cliente que puede realizar préstamos de libros.

    Attributes:
        nombre (CharField): Nombre del cliente.
        direccion (CharField): Dirección del cliente.
        telefono (CharField): Número de teléfono del cliente con formato chileno.
        correo (EmailField): Correo electrónico del cliente.
        usuario (ForeignKey): Relación con el modelo Usuario.
    """
    nombre = models.CharField(max_length=50, validators=[MinLengthValidator(3)])
    direccion = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    telefono = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^(?:\+56|56)?9\d{8}$',
                message='Teléfono incorrecto. Ejemplo: +56912345678'
            )
        ]
    )
    correo = models.EmailField(validators=[EmailValidator(message='Correo incorrecto.')])
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        Devuelve una representación en cadena del modelo.

        Returns:
            str: Nombre del cliente.
        """
        return self.nombre


class Libro(models.Model):
    """
    Representa un libro en la biblioteca.

    Attributes:
        isbn (CharField): Código ISBN único del libro.
        titulo (CharField): Título del libro.
        autor (CharField): Nombre del autor del libro.
        editorial (CharField): Nombre de la editorial del libro.
        anio_publicacion (BigIntegerField): Año de publicación del libro.
        disponibilidad (BooleanField): Indica si el libro está disponible.
        usuario (ForeignKey): Relación con el modelo Usuario.
        categorias (ManyToManyField): Relación con múltiples categorías.
    """
    isbn = models.CharField(max_length=100, unique=True)
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=50)
    editorial = models.CharField(max_length=50)
    anio_publicacion = models.BigIntegerField()
    disponibilidad = models.BooleanField(default=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    categorias = models.ManyToManyField(Categoria, related_name='libros')

    def __str__(self):
        """
        Devuelve una representación en cadena del modelo.

        Returns:
            str: Título del libro.
        """
        return self.titulo


class Prestamo(models.Model):
    """
    Representa un préstamo de un libro a un cliente.

    Attributes:
        fecha_prestamo (DateField): Fecha en la que se realizó el préstamo.
        fecha_devolucion (DateField): Fecha en la que se espera la devolución.
        estado (BooleanField): Indica si el préstamo está activo.
        cliente (ForeignKey): Relación con el modelo Cliente.
        libro (ForeignKey): Relación con el modelo Libro.
        categoria (ForeignKey): Relación con el modelo Categoria.
        usuario (ForeignKey): Relación con el modelo Usuario.
    """
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField()
    estado = models.BooleanField(default=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        Devuelve una representación en cadena del modelo.

        Returns:
            str: Información del préstamo, incluyendo el nombre del cliente.
        """
        return f"Préstamo - {self.cliente.nombre if self.cliente else 'Sin Cliente'}"

    