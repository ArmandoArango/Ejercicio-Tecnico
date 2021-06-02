from django.db import models
from django.db.models.fields import AutoField, CharField, EmailField

# Create your models here.
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User

DOC_CHOICESUSU = (
    ('AD', _(u"Administrador")),
    ('CLI', _(u"Cliente")),
)

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    rol = models.CharField(max_length=10, choices= DOC_CHOICESUSU, default='CLI')
    usuid = models.OneToOneField(User, on_delete=models.CASCADE)


class Foto(models.Model):
    id_foto = models.AutoField(primary_key=True)
    imagen = models.ImageField(upload_to='fotos')