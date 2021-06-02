from django import forms
from django.utils.translation import ugettext_lazy as _

from Usuario.models import Foto



DOC_CHOICESUSU = (
    ('AD', _(u"Administrador")),
    ('CLI', _(u"Cliente")),
)

class FotoForm(forms.ModelForm):
    class Meta:
        model = Foto
        fields = "__all__"
        labels = {
            'foto': _(u'foto'),
        }

    def __init__(self, *args, **kwargs):
        super(FotoForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class Registroform(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    email = forms.EmailField(max_length=150, label='Email')
    password = forms.CharField(max_length=128, label='Contraseña', widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=128, label='Confirmar Contraseña', widget=forms.PasswordInput())

    nombres = forms.CharField(max_length=50, label='Nombres')
    apellidos = forms.CharField(max_length=50, label='Apellidos')
    rol = forms.ChoiceField(choices=DOC_CHOICESUSU, label="Tipo de Usuario", widget=forms.Select())

    def __init__(self, *args, **kwargs):
        super(Registroform, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})