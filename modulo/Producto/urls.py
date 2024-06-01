from django.urls import path
from .views import listar, eliminar,principal,promociones,agregarProductos,crearOferta,agregarCategoria,modificar, respuesta_json

urlpatterns = [
    path('', principal, name='principal'),
    path('promociones',promociones,name='promociones'),
    path('agregarProductos',agregarProductos,name='agregarProductos'),
    path('crearOferta',crearOferta,name='crearOferta'),
    path('agregarCategoria',agregarCategoria,name='agregarCategoria'),
    path('Productos',listar,name = 'listarProducto'),
    path ('modificar /<int:idProducto> ',modificar,name='modificarProducto'),
    path ('eliminar /<int:idProducto> ',eliminar,name='eliminarProducto'),
    path('respuesta-json/', respuesta_json , name="respuesta_json")
]


