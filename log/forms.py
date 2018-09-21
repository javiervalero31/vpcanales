from django.contrib.auth.forms import AuthenticationForm
from django import forms

#Formulario para ingresar en el portal
class LoginForm(AuthenticationForm):
    #Este sera el IDOP
    username = forms.CharField(label="Ldap", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder':' Código de Empleado'}))
    #Password asignado para la contraseña
    password = forms.CharField(label="Contraseña", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder':' Contraseña'}))
