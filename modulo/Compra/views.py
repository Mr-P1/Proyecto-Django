from asyncio.windows_events import NULL
import datetime
from django.shortcuts import render 
from django.urls import reverse
from django.http import HttpResponseRedirect
from modulo.Compra.models import ESTADOS_ENVIO, Carrito, Detalle_compra ,Producto, Historial,Seguimiento2,Compra
from modulo.Usuario.models import Usuario, Suscripcion
from django.core.exceptions import ObjectDoesNotExist
import sweetify

# Create your views here.
def carroCompra(request):
    usuario = Usuario.objects.get(idUsuario__id =request.user.id )
    carrito = Carrito.objects.filter(idUsuario__id = usuario.id)
    
    total = 0
    for x in carrito:
        total += x.total
    contexto = {
        'carrito':carrito,
        'total':total
    }
    return render(request,'base/carro_compra.html',contexto)

def vaciarCarro(request):
    cliente = Usuario.objects.get(idUsuario = request.user.id)
    CarritoCliente = Carrito.objects.filter(idUsuario = cliente.id)
    CarritoCliente.delete()
    return HttpResponseRedirect(reverse('carroCompra'))



def agregar_carrito(request,producto_id ):
    productoEncontrado = Producto.objects.get(id = producto_id)
    usuario = Usuario.objects.get(idUsuario__id =request.user.id )
    print(productoEncontrado.id_Promocion.porc_descuento)
    try:
        producto_carrito = Carrito.objects.get(idProducto__id = productoEncontrado.id,idUsuario__id = usuario.id)
        print(producto_carrito)
        descuento2 = productoEncontrado.id_Promocion.porc_descuento / 100
        producto_carrito.cantidad = producto_carrito.cantidad + 1 
        producto_carrito.total = producto_carrito.cantidad * (producto_carrito.idProducto.precio * (1-descuento2) )
        producto_carrito.save()

    except Exception:

        nuevocarrito = Carrito()
        nuevocarrito.cantidad = 1
        descuento2 = productoEncontrado.id_Promocion.porc_descuento / 100
        nuevocarrito.total =(productoEncontrado.precio * (1-descuento2)) * nuevocarrito.cantidad
        nuevocarrito.idProducto = productoEncontrado
        nuevocarrito.idUsuario = usuario
        nuevocarrito.save()
    return HttpResponseRedirect(reverse('promociones'))

def agregar_carrito2(request,producto_id ):
    productoEncontrado = Producto.objects.get(id = producto_id)
    
    usuario = Usuario.objects.get(idUsuario__id =request.user.id )
    try :
        producto_carrito = Carrito.objects.get(idProducto__id = productoEncontrado.id,idUsuario__id = usuario.id)
        print(producto_carrito)
        producto_carrito.cantidad = producto_carrito.cantidad + 1 
        producto_carrito.total = producto_carrito.cantidad * producto_carrito.idProducto.precio
        producto_carrito.save()
    except Exception :
        nuevocarrito = Carrito()
        nuevocarrito.cantidad = 1
        nuevocarrito.total =productoEncontrado.precio * nuevocarrito.cantidad
        nuevocarrito.idProducto = productoEncontrado
        nuevocarrito.idUsuario = usuario
        nuevocarrito.save()
    return HttpResponseRedirect(reverse('principalUsuario'))
   
def eliminar_producto(request, carrito_id):
    carrito = Carrito.objects.get(id = carrito_id)
    carrito.delete()
    return HttpResponseRedirect(reverse('carroCompra'))




def dCompra(request,idDetalle_Compra):
    
    carritoe = Carrito.objects.get(id = idDetalle_Compra)
    contexto = {
        'carrito':carritoe
    }
    if request.method == 'POST':
        carritoe.delete()
        return HttpResponseRedirect(reverse('carroCompra'))
    return render(request,'base/carro_compra.html',contexto)


def histoCompra(request):

    usuario = Usuario.objects.get(idUsuario__id =request.user.id )
    compra = Compra.objects.filter(id_Usuario__id = usuario.id)
    
    contexto = {
        
        'historial':compra
    }
    return render(request,'base/historial_comp.html',contexto)

def seguimiento(request):
    usuario = Usuario.objects.get(idUsuario__id =request.user.id )
    seguimiento = Seguimiento2.objects.filter( idCompra__id_Usuario__id = usuario.id)
    #s2 = Seguimiento2.objects.filter( )

    contexto = {
        'seguimiento':seguimiento
    }
    return render(request,'base/seguimiento_comp.html',contexto)

def compra (request):
    cliente = Usuario.objects.get(idUsuario = request.user.id)
    carrito = Carrito.objects.filter(idUsuario__id =cliente.id)
    
    if request.method == 'GET':
            
        try :
            suscrito = Suscripcion.objects.get(id_usuario__idUsuario__id = request.user.id)
            porc = 0.05
        except ObjectDoesNotExist:
            porc = 0

        print(porc)
        total = 0
        for x in carrito:
            total += x.total
        total = round(total * (1-porc))
        contexto = {
            'cliente':cliente,
            'carrito':carrito,
            'total':total,
        }
    
        
        return render (request,'base/compra.html',contexto)

    elif request.method == 'POST':
        usuario = Usuario.objects.get(idUsuario__id =request.user.id )
        carrito = Carrito.objects.filter(idUsuario__id = usuario.id)
        compra = Compra()
        #historial = Historial()
        seguimiento = Seguimiento2()


        try :
            suscrito = Suscripcion.objects.get(id_usuario__idUsuario__id = request.user.id)
            porc = 0.05
        except ObjectDoesNotExist:
            porc = 0


        total_precio= 0
        total_cantidad = 0
        for x in carrito:
            total_precio += x.total
            total_cantidad += x.cantidad

        total_precio = round(total_precio *(1-porc))

        compra.Total_a_pagar = total_precio 
        compra.id_Usuario = usuario
        compra.cantidad_total = total_cantidad
       
        compra.save()
                    
        
        seguimiento.idCompra = compra
        seguimiento.hora = datetime.datetime.now()
        seguimiento.direccion = request.POST['direccion']   
        seguimiento.save()
        
        for x in carrito:
            detalle_compra =Detalle_compra()
            detalle_compra.cantidad =x.cantidad
            detalle_compra.Total = x.total
            detalle_compra.id_Producto = x.idProducto
            productoEncontrado = Producto.objects.get (id = detalle_compra.id_Producto.id)
            productoEncontrado.stock = productoEncontrado.stock - x.cantidad
            if productoEncontrado.stock <0 :
                productoEncontrado.stock = 0
            productoEncontrado.save()
            detalle_compra.id_Compra = compra
            detalle_compra.save()
            x.delete()
                        
            
    return HttpResponseRedirect (reverse('principalUsuario'))




def mas(request,id_p):
    
    usuario = Usuario.objects.get(idUsuario__id =request.user.id )
    producto_carrito = Carrito.objects.get(idProducto__id=id_p,idUsuario__id = usuario.id)
    descuento3 = producto_carrito.idProducto.id_Promocion.porc_descuento/ 100
    producto_carrito.cantidad =producto_carrito.cantidad + 1 
    producto_carrito.total = producto_carrito.cantidad * (producto_carrito.idProducto.precio * (1-descuento3) )
    producto_carrito.save()
    return HttpResponseRedirect (reverse('carroCompra'))

def menos(request,id_p):
    usuario = Usuario.objects.get(idUsuario__id =request.user.id )
    producto_carrito = Carrito.objects.get(idProducto__id=id_p,idUsuario__id = usuario.id)
    descuento3 = producto_carrito.idProducto.id_Promocion.porc_descuento/ 100
    producto_carrito.cantidad =producto_carrito.cantidad - 1 
    producto_carrito.total = producto_carrito.cantidad * (producto_carrito.idProducto.precio * (1-descuento3) )
    if producto_carrito.cantidad == 0:
        producto_carrito.delete()
    else:
        producto_carrito.save()
    return HttpResponseRedirect (reverse('carroCompra'))


def listarSeguimiento(request):
    
    seguimiento = Seguimiento2.objects.all()

    contexto = {
        'seguimiento':seguimiento
    }
    return render(request,'base/listarSeguimiento.html',context =contexto)

def cambiarSeguimiento(request,idSeguimiento):
    seguimiento = Seguimiento2.objects.get(id =idSeguimiento)
    
    if request.method == 'GET':
        contexto={
            'seguimiento' :seguimiento,
            'estados' :ESTADOS_ENVIO
        }
        return render(request, 'base/cambiarSeguimiento.html',contexto)

    elif request.method == 'POST': 
        seguimiento.procesoEnvio = request.POST['x']
        seguimiento.save()
        return HttpResponseRedirect (reverse ('listarSeguimiento'))


