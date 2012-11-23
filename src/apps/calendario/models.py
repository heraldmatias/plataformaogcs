# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import truncatewords
from usuario.models import Organismo, Usuario
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
class Evento(models.Model):
    codigo = models.AutoField(primary_key=True, db_index=True)
    organismo = models.ForeignKey(Organismo, verbose_name='Organismo')
    dependencia = models.IntegerField(verbose_name='Dependencia',)
    titulo = models.CharField(verbose_name='Titulo', max_length=200)
    descripcion = models.CharField(max_length=200)
    lugar = models.CharField(max_length=200)
    fec_inicio = models.DateField(default=datetime.today())
    hor_inicio = models.TimeField()
    fec_termin = models.DateField(default=datetime.today())
    hor_termin =  models.TimeField()
    url_edit = models.CharField(max_length=300, null=True, blank=True)
    idusuario_creac = models.ForeignKey(Usuario,verbose_name='Usuario creador',
    	related_name='ucreador')    
    fec_creac = models.DateTimeField(verbose_name='Fecha de creación del registro',auto_now_add=True)
    idusuario_mod = models.ForeignKey(Usuario,verbose_name='Usuario modifico',
    related_name='umodificador', null=True, blank=True)
    fec_mod = models.DateTimeField(verbose_name='Fecha modifico', null=True, blank=True)    
        
    def __unicode__(self):
        return truncatewords(self.titulo,10)

    #def save(self, *args, **kwargs):        
    #    if self.motivo_devolucion:
    #        self.motivo_devolucion = self.motivo_devolucion.replace('"',"'")
    #    super(Evento, self).save(*args, **kwargs) # Call the "real" save() method.

    class Meta:
        db_table = u'eventos'
        verbose_name = u'Evento'
        verbose_name_plural = u'Eventos'

@receiver(post_save, sender=Evento)
def my_handler(sender, **kwargs):
    #print kwargs['instance'].__dict__
    pass