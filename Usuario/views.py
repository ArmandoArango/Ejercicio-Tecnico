from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib import auth
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from Usuario.models import Foto, Usuario
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages

from Usuario.forms import Registroform, FotoForm
from Usuario.models import Foto

# Create your views here.

class Login(View):

    def get(self, request):
        return  render(request, 'login.html')

    def post(self, request):
        username = request.POST.get("signin_username", "")
        password = request.POST.get("signin_password", "")
        usuario = auth.authenticate(username=username,
                                    password=password)

        if usuario is not None and usuario.is_active:
            auth.login(request, usuario)
            datos_usu = Usuario.objects.filter(usuid= usuario.pk)

            if len(datos_usu) > 0:
                if datos_usu[0].rol == "AD":
                    return redirect('listar_foto')
                else:
                    messages.add_message(request, messages.ERROR, "No existe en el sistema")

        else:
            if usuario == None:
                messages.add_message(request, messages.ERROR, "El Usuario no existe en el Sistema")

            else:
                messages.add_message(request, messages.ERROR, "El Usuario esta inactivo")

        return render(request, 'login.html')


class Logout(View):

    def get(self, request):
        auth.logout(request)
        return HttpResponseRedirect(reverse('login'))


class RegistarUsuario(View):
    form_class = Registroform
    template_name = 'adicionar_cliente.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirm_password', None)

        nombres = request.POST.get('nombres', None)
        apellido = request.POST.get('apellidos', None)
        rol = request.POST.get('rol', None)


        if password == confirm_password:
            if username and email and password and confirm_password:
                user, created = User.objects.get_or_create(username=username,
                                                           email=email,
                                                           first_name=nombres,
                                                           last_name=apellido)

                if created:

                    user.set_password(password)
                    user.save()
                    usu = Usuario(nombre=nombres,apellido=apellido,rol=rol,usuid=user)
                    usu.save()
                    messages.add_message(request, messages.INFO, "El usuario se creo satisfactoriamente")
                    list = Login()
                    return list.get(request)

                else:
                    messages.add_message(request, messages.ERROR, "El usuario ya existe en el sistema")

            else:
                messages.add_message(request, messages.ERROR, "Faltan campos por llenar en el formulario")

        else:
            messages.add_message(request, messages.ERROR, "Verique las contraseña")

        form = self.form_class(request.POST)
        return render(request, self.template_name, {'form': form})


class Listar_foto(View, LoginRequiredMixin):
    login_url = '/'
    template_name = 'listar_fotos.html'

    def get(self, request):
        try:
            fotos = Foto.objects.all()
            return render(request,self.template_name,{"fotos": fotos})

        except Foto.DoesNotExist:
            return render(request, "pages-404.html")


class AdicionaFoto(LoginRequiredMixin, View):
    login_url = '/'
    form_class = FotoForm
    template_name = 'agregar_foto.html'

    def get(self, request):
            form = self.form_class()
            return render(request,
                          self.template_name, {'form': form})

    def post(self, request):
        try:
            form = self.form_class( request.POST, request.FILES)

            if form.is_valid():
                form.save()
                messages.add_message(request, messages.INFO, 'Se adicionó correctamente')

            else:
                messages.add_message(request, messages.ERROR, 'No se pudo adicionar')

            listar = Listar_foto()
            return listar.get(request)

        except Foto.DoesNotExist:
            return render(request, "pages-404.html")


class ModificaFoto(LoginRequiredMixin, View):
    login_url = '/'
    form_class = FotoForm
    template_name = 'modificar_foto.html'

    def get(self, request, id_foto):
        try:
            foto = Foto.objects.get(id_foto=id_foto)
            form = self.form_class(instance=foto)
            return render(request,self.template_name,{'form': form})

        except Foto.DoesNotExist:
            return render(request, "pages-404.html")


    def post(self, request, id_foto):
        try:
            foto = Foto.objects.get(id_foto=id_foto)
            form = self.form_class(request.POST, request.FILES, instance=foto)

            if form.is_valid():
                form.save()
                messages.add_message(request, messages.INFO, 'Se modificó correctamente')

            else:
                messages.add_message(request, messages.ERROR, 'No se pudo modificar')

            listar = Listar_foto()
            return listar.get(request)

        except Foto.DoesNotExist:
            return render(request, "pages-404.html")


class VisualizaFoto(LoginRequiredMixin, View):
    login_url = '/'
    form_class = FotoForm
    template_name = 'visualizar_foto.html'

    def get(self, request, id_foto):
        try:
            foto = Foto.objects.get(id_foto=id_foto)
            form = self.form_class(instance=foto)
            return render(request,self.template_name,{'form': form})

        except Foto.DoesNotExist:
            return render(request, "pages-404.html")


class BorraFoto(LoginRequiredMixin, View):
    login_url = '/'
    form_class = FotoForm
    template_name = 'eliminar_foto.html'

    def get(self, request, id_foto):
        try:
            foto = Foto.objects.get(id_foto=id_foto)
            form = self.form_class(instance=foto)
            return render(request,self.template_name,{'form': form})

        except Foto.DoesNotExist:
            return render(request, "pages-404.html")

    def post(self, request, id_foto):
        try:
            foto = Foto.objects.get(id_foto=id_foto)
            foto.delete()
            messages.add_message(request, messages.INFO, "Se borró correctamente")
            listar = Listar_foto()
            return listar.get(request)

        except Foto.DoesNotExist:
            return render(request, "pages-404.html")