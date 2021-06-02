
from django.conf.urls import include, url
from django.contrib import admin
from Usuario.views import Login
from Usuario.views import Logout
from Usuario.views import RegistarUsuario
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from Usuario.views import Listar_foto,AdicionaFoto, ModificaFoto, VisualizaFoto, BorraFoto

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Login.as_view(), name='login'),
    url(r'^registro/', RegistarUsuario.as_view(), name='registro'),
    url(r'^listar_foto/', Listar_foto.as_view(), name='listar_foto'),
    url(r'^adicionar_foto/', AdicionaFoto.as_view(), name='adicionar_foto'),
    url(r'^modificar_foto/(?P<id_foto>\w+)', ModificaFoto.as_view(), name='modificar_foto'),
    url(r'^visualizar_foto/(?P<id_foto>\w+)', VisualizaFoto.as_view(), name='visualizar_foto'),
    url(r'^borrar_foto/(?P<id_foto>\w+)', BorraFoto.as_view(), name='borrar_foto'),
    url(r'logout/', Logout.as_view(), name='logout'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
