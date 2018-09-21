from django.db import models

# Create your models here.


class Direccion(models.Model):
	nombre_dir=models.CharField(max_length=50)
	def __str__(self):
		return self.nombre_dir


class Coordinador(models.Model):
	nombre_coord = models.CharField(max_length=255,null=True)
	activo=models.BooleanField(default=False)

	def __str__(self):
		return self.nombre_coord


class Gerente(models.Model):
	nombre_gte = models.CharField(max_length=255)
	activo=models.BooleanField(default=False)

	def __str__(self):

		return self.nombre_gte


class Estado(models.Model):
	estado= models.CharField(max_length=255)

	def __str__(self):
		return self.estado


class Region(models.Model):
	region = models.CharField(max_length=255)

	def __str__(self):
		return self.region

class Ubicacion(models.Model):
	estado_key = models.ForeignKey(Estado,on_delete=models.CASCADE)
	region_key = models.ForeignKey(Region,on_delete=models.CASCADE)
	direccion_key = models.ForeignKey(Direccion,on_delete=models.CASCADE)

	def __str__(self):
		return str(self.estado_key)

class Supervisor(models.Model):
	nombre_super = models.CharField(max_length=255,null=True)
	activo=models.BooleanField(default=False)

	def __str__(self):
		return self.nombre_super


class Jerarquia(models.Model):
	gerente_key = models.ForeignKey(Gerente,on_delete=models.CASCADE)
	coordinador_key = models.ForeignKey(Coordinador,on_delete=models.CASCADE,null=True)
	supervisor_key = models.ForeignKey(Supervisor,on_delete=models.CASCADE,null=True)
	activo = models.BooleanField(default=False)

	def __str__(self):
		return str(self.gerente_key)


class Local(models.Model):
	codigo = models.CharField(max_length=50)
	nombre_local = models.CharField(max_length=255,null=True)
	codigo_sap = models.CharField(max_length=70,null=True)
	cc =  models.CharField(max_length=50)
	canal=models.CharField(max_length=30)
	activo=models.BooleanField(default=False)
	direccion_fisica = models.CharField(max_length=255)

	jerarquia=models.ForeignKey(Jerarquia,on_delete=models.CASCADE)
	ubicacion=models.ForeignKey(Ubicacion,on_delete=models.CASCADE)

	def __str__(self):
		return self.codigo


class Homologador(models.Model):
	homologador = models.CharField(max_length=255)

	def __str__(self):
		return self.homologador


class Plan(models.Model):
	codigo_plan = models.CharField(max_length=20)
	nombre_plan = models.CharField(max_length=255)

	def __str__(self):
		return self.nombre_plan



class ProduccionPlan(models.Model):
	fecha_prod =  models.DateField()
	homologador = models.ForeignKey(Homologador,on_delete=models.CASCADE)
	plan = models.ForeignKey(Plan,on_delete=models.CASCADE)
	renta_mensual = models.FloatField()
	recarga_plan = models.FloatField()

	def __str__(self):
		return str(self.plan)


class Activacion(models.Model):
	fecha_carga=models.DateField(auto_now_add=True)
	fecha_actividad=models.DateField()
	plataforma=models.CharField(max_length=50)
	tecnologia=models.CharField(max_length=50)
	terminal=models.CharField(max_length=50)
	cantidad=models.FloatField()
	plan_key=models.ForeignKey(ProduccionPlan,on_delete=models.CASCADE,null=True)
	local_key=models.ForeignKey(Local,on_delete=models.CASCADE,null=True)


	def __str__(self):
		return "ACT %s Descrp: CodVend=%s Tecnolg=%s " %(self.cantidad, self.local_key,self.tecnologia)


class Alta(models.Model):
	fecha_carga=models.DateField(auto_now_add=True)
	fecha_actividad=models.DateField()
	plataforma=models.CharField(max_length=50)
	tecnologia=models.CharField(max_length=50)
	terminal=models.CharField(max_length=50)
	cantidad=models.IntegerField()
	plan_key=models.ForeignKey(ProduccionPlan,on_delete=models.CASCADE,null=True)
	local_key=models.ForeignKey(Local,on_delete=models.CASCADE,null=True)

	def __str__(self):
		return "ALTA %s Descrp: CodVend=%s Tecnolg=%s " %(self.cantidad, self.local_key,self.tecnologia)



class Baja(models.Model):
	fecha_carga=models.DateField(auto_now_add=True)
	fecha_actividad=models.DateField()
	plataforma=models.CharField(max_length=50)
	tecnologia=models.CharField(max_length=50)
	terminal=models.CharField(max_length=50)
	bruta=models.IntegerField()
	neta=models.IntegerField()
	reactivada=models.IntegerField()
	plan_key=models.ForeignKey(ProduccionPlan,on_delete=models.CASCADE,null=True)
	local_key=models.ForeignKey(Local,on_delete=models.CASCADE,null=True)
	def __str__(self):
		return("BAJAS: BRUTAS = %s NETAS = %s REACTIVADAS = %s para Local = %s") %(self.bruta,self.neta,self.reactivada)




class Cuota(models.Model):
	fecha_carga=models.DateField(auto_now_add=True)
	fecha_cuota=models.DateField()
	local_key=models.ForeignKey(Local,on_delete=models.CASCADE,null=True)

	cuota_activaciones_total = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_altas_total = models.DecimalField(max_digits=12, decimal_places=6)

	cuota_activaciones_sp = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_activaciones_nosp = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_activaciones_prepago = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_activaciones_pospago = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_activaciones_spmp = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_activaciones_spme = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_activaciones_nospmp = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_activaciones_nospme = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_activaciones_spprepago = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_activaciones_sppospago = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_activaciones_nospprepago = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_activaciones_nosppospago = models.DecimalField(max_digits=12, decimal_places=6)

	cuota_altas_sp = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_altas_nosp = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_altas_prepago = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_altas_pospago = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_altas_spmp = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_altas_spme = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_altas_nospmp = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_altas_nospme = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_altas_spprepago = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_altas_sppospago = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_altas_nospprepago = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_altas_nosppospago = models.DecimalField(max_digits=12, decimal_places=6)

	cuota_cater_spmp = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_cater_spme = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_cater_nospmp = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_cater_nospme = models.DecimalField(max_digits=12, decimal_places=6)

	cuota_tvhd = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_tvsd = models.DecimalField(max_digits=12, decimal_places=6)
	cuota_fijo = models.DecimalField(max_digits=12, decimal_places=6)

	def __str__(self):
		return("Fecha Cuota: %s  ; Local: %s") %(self.fecha_cuota,self.local_key)
