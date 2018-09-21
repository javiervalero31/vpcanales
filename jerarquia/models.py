from django.db import models
from django.contrib.auth.models import User

class Tipo(models.Model):
	tipo=models.CharField(max_length=5)
	ldap = models.ForeignKey(User, null=True)
	def __str__(self):
		return self.tipo

class TipoAa(models.Model):
	tipo_aa=models.CharField(max_length=100)
	ldap = models.ForeignKey(User, null=True)
	def __str__(self):
		return self.tipo_aa

class Oficina(models.Model):
	oficina=models.CharField(max_length=25)
	ldap = models.ForeignKey(User, null=True)
	def __str__(self):
		return self.oficina

class Rif(models.Model):
	rif=models.CharField(max_length=10)
	ldap = models.ForeignKey(User, null=True)
	def __str__(self):
		return self.rif

class CodigoDeudor(models.Model):
	codigo_deudor=models.CharField(max_length=10)
	ldap = models.ForeignKey(User, null=True)
	def __str__(self):
		return self.codigo_deudor

class Nombre(models.Model):
	nombre=models.CharField(max_length=100)
	ldap = models.ForeignKey(User, null=True)
	def __str__(self):
		return self.nombre

class Direccion(models.Model):
	direccion=models.CharField(max_length=1000)
	ldap = models.ForeignKey(User, null=True)
	def __str__(self):
		return self.direccion

class Region(models.Model):
	region=models.CharField(max_length=25)
	ldap = models.ForeignKey(User, null=True)
	def __str__(self):
		return self.region

class Gerente(models.Model):
	gerente=models.CharField(max_length=50)
	ldap = models.ForeignKey(User, null=True)
	def __str__(self):
		return self.gerente

class Lider(models.Model):
	lider=models.CharField(max_length=50)
	ldap = models.ForeignKey(User, null=True)
	def __str__(self):
		return self.lider

class Coordinador(models.Model):
	coordinador=models.CharField(max_length=50)
	ldap = models.ForeignKey(User, null=True)
	def __str__(self):
		return self.coordinador


class CentroRecarga(models.Model):
	centro_recarga=models.CharField(max_length=50)
	ldap = models.ForeignKey(User, null=True)
	def __str__(self):
		return self.centro_recarga


class Distribuidor(models.Model):
	distribuidor=models.CharField(max_length=200)
	ldap = models.ForeignKey(User, null=True)
	def __str__(self):
		return self.distribuidor


class Status(models.Model):
	status=models.CharField(max_length=200)
	ldap = models.ForeignKey(User, null=True)
	def __str__(self):
		return self.status


class Estados(models.Model):
    id_estado = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=250)
    def __str__(self):
        return self.estado


class Ciudades(models.Model):
    id_ciudad = models.AutoField(primary_key=True)
    id_estado = models.ForeignKey(Estados, db_column='id_estado')
    ciudad = models.CharField(max_length=200)
    capital = models.SmallIntegerField()
    def __str__(self):
        return str(self.ciudad, self.capital)

class Municipios(models.Model):
    id_municipio = models.AutoField(primary_key=True)
    id_estado = models.ForeignKey(Estados, db_column='id_estado')
    municipio = models.CharField(max_length=100)
    def __str__(self):
        return str(self.municipio)

class Parroquias(models.Model):
    id_parroquia = models.AutoField(primary_key=True)
    id_municipio = models.ForeignKey(Municipios, db_column='id_municipio')
    parroquia = models.CharField(max_length=250)
    def __str__(self):
        return self.parroquia


class Historico(models.Model):
	a000sap = models.CharField(max_length=25,null=True)
	codigo_unico = models.CharField(max_length=25,null=True)
	visitas = models.IntegerField(null=True)
	latitud = models.FloatField(null=True)
	longitud = models.FloatField(null=True)
	direccion_fisica = models.CharField(max_length=2000,null=True)
	direccion_fiscal = models.CharField(max_length=2000,null=True)
	persona_contacto = models.CharField(max_length=70,null=True)
	correo_tienda = models.CharField(max_length=70,null=True)
	correo_empresario = models.CharField(max_length=70,null=True)
	telefono_empresario = models.CharField(max_length=20,null=True)
	telefono_tienda = models.CharField(max_length=20,null=True)
	hora_apertura = models.TimeField(null=True)
	hora_cierre = models.TimeField(null=True)
	empleados = models.IntegerField(null=True)
	punto_rojo = models.BooleanField()
	caso_remedy = models.CharField(max_length=25,null=True)
	# sustitucion = models.CharField(max_length=25,null=True)
	fecha = models.DateField(null=True)
	enero = models.BooleanField(default=False)
	febrero = models.BooleanField(default=False)
	marzo = models.BooleanField(default=False)
	abril = models.BooleanField(default=False)
	mayo = models.BooleanField(default=False)
	junio = models.BooleanField(default=False)
	julio = models.BooleanField(default=False)
	agosto = models.BooleanField(default=False)
	septiembre = models.BooleanField(default=False)
	octubre = models.BooleanField(default=False)
	noviembre = models.BooleanField(default=False)
	diciembre = models.BooleanField(default=False)
	municipio_key = models.ForeignKey(Municipios, on_delete=models.CASCADE,null=True)
	estado_key = models.ForeignKey(Estados, on_delete=models.CASCADE,null=True)
	tipo_key = models.ForeignKey(Tipo,on_delete=models.CASCADE,null=True)
	tipo_aa_key = models.ForeignKey(TipoAa,on_delete=models.CASCADE,null=True)
	oficina_key = models.ForeignKey(Oficina,on_delete=models.CASCADE,null=True)
	codigo_deudor_key = models.ForeignKey(CodigoDeudor,on_delete=models.CASCADE,null=True)
	nombre_key = models.ForeignKey(Nombre,on_delete=models.CASCADE,null=True)
	direccion_key = models.ForeignKey(Direccion,on_delete=models.CASCADE,null=True)
	region_key = models.ForeignKey(Region,on_delete=models.CASCADE,null=True)
	coordinador_key = models.ForeignKey(Coordinador,on_delete=models.CASCADE,null=True)
	lider_key = models.ForeignKey(Lider,on_delete=models.CASCADE,null=True)
	gerente_key = models.ForeignKey(Gerente,on_delete=models.CASCADE,null=True)
	centro_recarga_key = models.ForeignKey(CentroRecarga,on_delete=models.CASCADE,null=True)
	distribuidor_key = models.ForeignKey(Distribuidor,on_delete=models.CASCADE,null=True)
	status_key = models.ForeignKey(Status,on_delete=models.CASCADE,null=True)
	rif_key  = models.ForeignKey(Rif,on_delete=models.CASCADE,null=True)
	def __str__(self):
		return str(self.codigo_unico)

class Temporal(models.Model):
	a000sap = models.CharField(max_length=25,null=True)
	codigo_unico = models.CharField(max_length=25,null=True)
	visitas = models.IntegerField(null=True)
	latitud = models.CharField(max_length=20,null=True)
	longitud = models.CharField(max_length=20,null=True)
	direccion_fisica = models.CharField(max_length=2000,null=True)
	direccion_fiscal = models.CharField(max_length=2000,null=True)
	estado_key = models.ForeignKey(Estados, on_delete=models.CASCADE,null=True)
	municipio_key = models.ForeignKey(Municipios, on_delete=models.CASCADE,null=True)
	persona_contacto = models.CharField(max_length=70,null=True)
	correo_tienda = models.CharField(max_length=70,null=True)
	correo_empresario = models.CharField(max_length=70,null=True)
	telefono_empresario = models.CharField(max_length=20,null=True)
	telefono_tienda = models.CharField(max_length=20,null=True)
	hora_apertura = models.TimeField(null=True)
	hora_cierre = models.TimeField(null=True)
	empleados = models.IntegerField(null=True)
	punto_rojo = models.BooleanField(default=False)
	caso_remedy = models.CharField(max_length=25,null=True,blank=True)
	# sustitucion = models.CharField(max_length=25,null=True,blank=True)
	enero = models.BooleanField(default=False)
	febrero = models.BooleanField(default=False)
	marzo = models.BooleanField(default=False)
	abril = models.BooleanField(default=False)
	mayo = models.BooleanField(default=False)
	junio = models.BooleanField(default=False)
	julio = models.BooleanField(default=False)
	agosto = models.BooleanField(default=False)
	septiembre = models.BooleanField(default=False)
	octubre = models.BooleanField(default=False)
	noviembre = models.BooleanField(default=False)
	diciembre = models.BooleanField(default=False)
	tipo_key = models.ForeignKey(Tipo,on_delete=models.CASCADE,null=True)
	tipo_aa_key = models.ForeignKey(TipoAa,on_delete=models.CASCADE,null=True)
	oficina_key = models.ForeignKey(Oficina,on_delete=models.CASCADE,null=True)
	codigo_deudor_key = models.ForeignKey(CodigoDeudor,on_delete=models.CASCADE,null=True)
	nombre_key = models.ForeignKey(Nombre,on_delete=models.CASCADE,null=True)
	direccion_key = models.ForeignKey(Direccion,on_delete=models.CASCADE,null=True)
	region_key = models.ForeignKey(Region,on_delete=models.CASCADE,null=True)
	coordinador_key = models.ForeignKey(Coordinador,on_delete=models.CASCADE,null=True)
	lider_key = models.ForeignKey(Lider,on_delete=models.CASCADE,null=True)
	gerente_key = models.ForeignKey(Gerente,on_delete=models.CASCADE,null=True)
	centro_recarga_key = models.ForeignKey(CentroRecarga,on_delete=models.CASCADE,null=True,blank=True)
	distribuidor_key = models.ForeignKey(Distribuidor,on_delete=models.CASCADE,null=True,blank=True)
	status_key = models.ForeignKey(Status,on_delete=models.CASCADE,null=True)
	rif_key = models.ForeignKey(Rif,on_delete=models.CASCADE,null=True)
	ldap = models.ForeignKey(User, null=True)
	def __str__(self):
		return str(self.codigo_unico)

class Cambio(models.Model):
	a000sap = models.CharField(max_length=25)
	codigo_unico = models.CharField(max_length=25)
	visitas = models.IntegerField()
	latitud = models.FloatField()
	longitud = models.FloatField()
	direccion_fisica = models.CharField(max_length=2000)
	direccion_fiscal = models.CharField(max_length=2000)
	estado_key = models.ForeignKey(Estados, on_delete=models.CASCADE,null=True)
	municipio_key = models.ForeignKey(Municipios, on_delete=models.CASCADE,null=True)
	persona_contacto = models.CharField(max_length=70)
	correo_tienda = models.CharField(max_length=70)
	correo_empresario = models.CharField(max_length=70)
	telefono_empresario = models.CharField(max_length=20)
	telefono_tienda = models.CharField(max_length=20)
	hora_apertura = models.TimeField()
	hora_cierre = models.TimeField()
	empleados = models.IntegerField()
	punto_rojo = models.BooleanField(default=False)
	caso_remedy = models.CharField(max_length=25)
	# sustitucion = models.CharField(max_length=25, null)
	aprobacion_1 = models.CharField(max_length=25, null=True)
	aprobacion_2 = models.CharField(max_length=25, null=True)
	rechazado = models.CharField(max_length=25, null=True)
	idop_solicitante = models.CharField(max_length=10)
	fecha_solicitud = models.DateField(auto_now_add=True)
	enero = models.BooleanField(default=False)
	febrero = models.BooleanField(default=False)
	marzo = models.BooleanField(default=False)
	abril = models.BooleanField(default=False)
	mayo = models.BooleanField(default=False)
	junio = models.BooleanField(default=False)
	julio = models.BooleanField(default=False)
	agosto = models.BooleanField(default=False)
	septiembre = models.BooleanField(default=False)
	octubre = models.BooleanField(default=False)
	noviembre = models.BooleanField(default=False)
	diciembre = models.BooleanField(default=False)
	tipo_key = models.ForeignKey(Tipo,on_delete=models.CASCADE,null=True)
	tipo_aa_key = models.ForeignKey(TipoAa,on_delete=models.CASCADE,null=True)
	oficina_key = models.ForeignKey(Oficina,on_delete=models.CASCADE,null=True)
	codigo_deudor_key = models.ForeignKey(CodigoDeudor,on_delete=models.CASCADE,null=True)
	nombre_key = models.ForeignKey(Nombre,on_delete=models.CASCADE,null=True)
	direccion_key = models.ForeignKey(Direccion,on_delete=models.CASCADE,null=True)
	region_key = models.ForeignKey(Region,on_delete=models.CASCADE,null=True)
	coordinador_key = models.ForeignKey(Coordinador,on_delete=models.CASCADE,null=True)
	lider_key = models.ForeignKey(Lider,on_delete=models.CASCADE,null=True)
	gerente_key = models.ForeignKey(Gerente,on_delete=models.CASCADE,null=True)
	centro_recarga_key = models.ForeignKey(CentroRecarga,on_delete=models.CASCADE,null=True)
	distribuidor_key = models.ForeignKey(Distribuidor,on_delete=models.CASCADE,null=True)
	status_key = models.ForeignKey(Status,on_delete=models.CASCADE,null=True)
	rif_key  = models.ForeignKey(Rif,on_delete=models.CASCADE,null=True)
	def __str__(self):
		return str(self.codigo_unico)
