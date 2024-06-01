from distutils.log import error
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from modulo.Usuario.models import  Usuario , Suscripcion
from .models import User
from modulo.Producto.models import Categoria, Producto
import datetime
from django.db.models import Q
import sweetify
from .serializers import SuscripcionSeializer
# Create your views here.
def admin(request):
    return render(request,'base/administrador.html')

def listar(request):
    usuarios = User.objects.all()

    contexto = {
        'usuarios':usuarios
    }
    return render(request,'base/listarUsuario.html', context = contexto)

def suscripcion(request):
    
    usuario = Usuario.objects.get(idUsuario = request.user.id)
    
    contexto= {
        'usuario' :usuario
        }
    
    if request.method == 'GET':
        return render(request,'base/suscribirse.html',contexto) 
 
    elif request.method == 'POST':
        contexto = {}
        
        nuevoSuscriptor = usuario
        nuevoSuscriptor.id
        nuevoS= Suscripcion()
        nuevoS.f_suscripcion = datetime.datetime.now()
        nuevoS.monto = request.POST['monto']
        nuevoS.id_usuario =  Usuario.objects.get(id = nuevoSuscriptor.id)
        if  int( nuevoS.monto )>= 5000:
            if int ( nuevoS.monto )>= 100000:
                sweetify.warning(request,'El monto es muy alto')
            else:
                nuevoS.save()
                return HttpResponseRedirect(reverse('principalUsuario'))
            
        else:
            sweetify.warning(request, 'El monto debe ser igual ó mayor a 5000')
            return render(request,'base/suscribirse.html',contexto) 
    return render(request,'base/suscribirse.html',contexto)


def desuscribirse(request):
    if request.method == 'GET':
        return render(request,'base/DeSuscribirse.html')
    
    elif request.method == 'POST':
        cliente = Usuario.objects.get(idUsuario = request.user.id)
        Suscrito = Suscripcion.objects.filter(id_usuario = cliente.id)
        Suscrito.delete()
        return HttpResponseRedirect(reverse('principalUsuario'))
    
        
def registrarse(request):
    if request.method == 'GET':
        return render(request,'base/Registrarse.html')
        
    elif request.method =='POST':
        usuario = request.POST['usuario']
        contrasenia = request.POST['contrasenia']
        correo = request.POST['correo']
        try:
            usuario_creado, se_creo = User.objects.get_or_create(
                                        username = usuario,
                                        password = contrasenia,
                                        email = correo
                                        )          #el usuario es unico, por si lo duplico dara error
        except Exception as ex:
            codigo_error =int (ex.args[0])
            if codigo_error == 1062:
                
             sweetify.warning(request, 'Usuario ya existe, no se creo :C') 
    
            return render(request,'base/Registrarse.html')

    contexto = {}
    if se_creo:
        usuario_creado.set_password(contrasenia)
        usuario_creado.save()
        nuevoUsuario = Usuario()
        nuevoUsuario.idUsuario = usuario_creado
        nuevoUsuario.tipo_cuenta = 'Usuario'
        nuevoUsuario.save()
        return HttpResponseRedirect(reverse('iniciarsesion'))
        
    else:
        sweetify.warning(request, 'Usuario ya existe, no se creo :C') 
    return render(request,'base/Registrarse.html',contexto)


def iniciarsesion(request):
    if request.method =='GET':
        return render(request,'base/IniciarSesion.html')
    elif request.method =='POST':
        contexto={} 
        usuario = request.POST['usuario']
        contrasenia = request.POST['contrasenia']

        usuario_encontrado = authenticate(username = usuario,password = contrasenia)
        if usuario_encontrado is not None:
            login(request,usuario_encontrado)
            return HttpResponseRedirect(reverse('principalUsuario'))

        else:
            sweetify.warning(request, 'Usuario y contraseña no existen :C') 
        
        return render(request,'base/IniciarSesion.html',contexto)    



def eliminarSuscriptor(request):
    if request.method == 'GET':
        return render(request,'base/listarUsuario.html')

    elif request.method == 'POST':
        contexto = {}
        usuario = request.POST['User']

        try:
            usuario_econtrado = User.objects.get(username = usuario )

        except User.DoesNotExist:
            contexto['mensaje'] = "Usuario no encontrado"
            return render(request,'base/listarUsuario.html',contexto)

        if request.method == 'POST':
            usuario_econtrado.f_termino = datetime.datetime.now()
    return render(request,'base/ingresar.s.html')

def ingresarSuscriptor(request):
    if request.method == 'GET':
        return render(request,'base/ingresar.s.html') 

    elif request.method == 'POST':
        contexto = {}
        usuario = request.POST['User']
        
        try:
            usuario_econtrado = User.objects.get(username = usuario )
            usuario_econtrado.id
            usuario2 = Usuario.objects.get(idUsuario_id = usuario_econtrado.id)
            nuevoS= Suscripcion()
            nuevoS.f_suscripcion = datetime.datetime.now()
            nuevoS.monto = 0
            nuevoS.id_usuario =  Usuario.objects.get(id  = usuario2.id  )
            nuevoS.save()
            sweetify.success(request, 'Usuario ingresado con éxito!!!') 
            return render(request,'base/ingresar.s.html') 
           
        except User.DoesNotExist:
            sweetify.warning(request, 'Usuario no encontrado')  
            return render(request,'base/ingresar.s.html',contexto) 
    return render(request,'base/ingresar.s.html') 

def vigencia (request):
    vigentes  = Suscripcion.objects.all()
    contexto = { 
        'vigentes':vigentes
    }
   
    return render(request,'base/Vigencia.html',contexto)

def eliminar_suscriptor(request,id_s):
    suscriptor = Suscripcion.objects.get( id = id_s)
    suscriptor.delete()
    sweetify.success(request, 'Suscriptor Eliminado con éxito!!!') 
    return HttpResponseRedirect(reverse('vigencia'))
# hay que agregar esto a las urls 

def cerrar_sesion(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse('principal')) 


def principalUsuario (request):
    usuario = Usuario.objects.get(idUsuario__id =request.user.id )
    suscripcion  = Suscripcion.objects.filter(id_usuario__id = usuario.id)
    #suscripcion  = Suscripcion.objects.all()
    productos = Producto.objects.all()
    categoria = Categoria.objects.all()

    contexto = {
        'productos' : productos,
        'suscripcion' : suscripcion,
        'categorias' :categoria
    }
    
    buscar = ""
    try:
        buscar = request.GET["buscar"]
    except Exception:
        pass
    if request.method == "GET":
        
        productos = Producto.objects.filter(descripcion__contains=buscar)
        usuario_json = SuscripcionSeializer(suscripcion, many=True)
        print(usuario_json.data)
        contexto["productos"] = productos
    return render(request,'base/casoUsuario.html',contexto)

def listaCategoria(request,idCate):
    contexto={}
    busqueda = request.POST.get("buscador")
    listaCat = Producto.objects.filter(id_categoria = idCate)
    if busqueda:
        listaCat = Producto.objects.filter(
            Q(descripcion__contains=busqueda)
        ).distinct()

    data ={'entity':listaCat}
    contexto["productos"] = listaCat
    return render(request,'base/casoUsuario.html',contexto)

def usuario_json(request):
    if request.method == "GET":
        usuarios= Suscripcion.objects.all()
        usuario_json = SuscripcionSeializer(usuarios, many=True)
    return JsonResponse(usuario_json.data, safe=False)
    