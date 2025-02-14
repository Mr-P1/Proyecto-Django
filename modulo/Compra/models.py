from tkinter.tix import MAX
from django.db import models
from modulo.Usuario.models import Usuario
from modulo.Producto.models import Producto

# Create your models here.

ESTADO_PROCESO = 'EP' 
ESTADO_ENVIADO = 'EE' 
ESTADO_FINALIZADO = 'EF' 
ESTADOS_ENVIO = (
    (ESTADO_PROCESO , 'Preparacion'),
    (ESTADO_ENVIADO , 'Enviado'),
    (ESTADO_FINALIZADO, 'Finalizado'),

)



class Compra(models.Model):
    F_compra=models.DateField(auto_now=True)
    Hora_compra=models.DateTimeField(auto_now=True)
    Total_a_pagar=models.PositiveIntegerField()
    cantidad_total = models.PositiveIntegerField()
    id_Usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE)
    
class Detalle_compra(models.Model): 
    cantidad=models.PositiveIntegerField()
    Total=models.PositiveIntegerField()
    id_Producto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    id_Compra=models.ForeignKey(Compra,on_delete=models.CASCADE)

class Seguimiento2(models.Model):
    fecha =models.DateField(auto_now=True)
    hora =models.DateTimeField()
    direccion = models.CharField(max_length = 30 ,default="o")
    procesoEnvio= models.CharField(max_length=12,choices=ESTADOS_ENVIO,default=ESTADO_PROCESO)
    idCompra = models.ForeignKey(Compra,on_delete=models.CASCADE)
    


class Carrito(models.Model):
    cantidad= models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    idProducto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    idUsuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)

class Historial(models.Model):
    descripcion = models.CharField(max_length=40)
    fecha = models.DateField(auto_now=True)
    cantidad = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    idUsuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)



class Seguimiento(models.Model):
    fecha =models.DateField()
    hora =models.DateTimeField()
    estado_compra =models.CharField( max_length=10,default='En proceso'
    )
    idHistorial = models.ForeignKey(Historial,on_delete=models.CASCADE)