from django import forms
from AppBiblioteca.models import Usuario

class formularioLogin(forms.Form):
    rut = forms.CharField(max_length=12)
    contrasena = forms.CharField(max_length=100)

class FormularioRegister(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = "__all__"