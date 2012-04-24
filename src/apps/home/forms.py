# -*- coding: utf-8 -*-

from django import forms

class LoginForm(forms.Form):
    usuario = forms.CharField(max_length=45, label='E-mail:', widget=forms.TextInput(attrs={'placeholder':'Ingrese su usuario'}),)
    clave = forms.CharField(max_length=40, label='Contraseña:', widget=forms.PasswordInput(attrs={'placeholder':'Ingrese su contraseña'}),)
    
