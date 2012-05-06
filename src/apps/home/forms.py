# -*- coding: utf-8 -*-

from django import forms

class LoginForm(forms.Form):
    usuario = forms.CharField(max_length=45, label='E-mail:', widget=forms.TextInput(attrs={'placeholder':'Ingrese su usuario','style':'width:430px;height:15px;color:#8f8f8f'}),)
    clave = forms.CharField(max_length=40, label='Contraseña:', widget=forms.PasswordInput(attrs={'placeholder':'Ingrese su contraseña','style':'width:430px;height:15px;color:#8f8f8f'}),)
    
