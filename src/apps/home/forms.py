# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.template import Context, loader
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.utils.http import int_to_base36

class LoginForm(forms.Form):
    usuario = forms.CharField(max_length=45, label='E-mail:', widget=forms.TextInput(attrs={'placeholder':'Ingrese su usuario','style':'width:430px;height:15px;color:#141313'}),)
    clave = forms.CharField(max_length=40, label='Contraseña:', widget=forms.PasswordInput(attrs={'placeholder':'Ingrese su contraseña','style':'width:430px;height:15px;color:#141313'}),)


class PasswordResetFormHtml(PasswordResetForm):
    
    def save(self, domain_override=None, email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator, from_email=None, request=None):
        """
        Genera un link de un solo uso para resetear la contraseña y se envia al correo del usuario
        """
        from django.core.mail import EmailMessage
        from django.conf import settings
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            t = loader.get_template(email_template_name)
            c = {
                'email': user.email,
                'usuario': user,
                'domain': domain,
                'static':settings.STATIC_URL,
                'site_name': site_name,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            msg = EmailMessage(u"Reestablecimiento de contraseña en la Plataforma Intersectorial de Comunicación",t.render(Context(c)),from_email, [user.email])
            msg.content_subtype = "html"
            msg.send()

    
