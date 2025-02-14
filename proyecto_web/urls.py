from django.contrib import admin
from django.urls import path,include
from django.conf import global_settings as settings 
from django.conf.urls import static
from django.conf import settings
from django.conf.urls.static import static


from modulo.Usuario.urls import urlpatterns as urlusuario
from modulo.Compra.urls import urlpatterns as urlcompra
from modulo.Producto.urls import urlpatterns as urlproducto

urlpatterns = [
    path('',include(urlproducto)),
    path('admin/',include(urlusuario)),
    path('compra/',include(urlcompra)),
    path('producto/',include(urlproducto))
]


if settings.DEBUG == True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
