<<<<<<< Updated upstream
=======
from django import forms
from AppBiblioteca.models import Usuario, Libro

class formularioLogin(forms.Form):
    rut = forms.CharField(max_length=12)
    contrasena = forms.CharField(max_length=100)

class FormularioRegister(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = "__all__"
        
class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['isbn', 'titulo', 'autor', 'editorial', 'anio_publicacion', 'disponibilidad', 'usuario', 'categorias']
>>>>>>> Stashed changes
