from django import forms

class formularioLogin(forms.Form):
    rut = forms.CharField(max_length=12)
    contrasena = forms.CharField(max_length=100)