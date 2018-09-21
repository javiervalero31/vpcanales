from django.shortcuts import render
from .models import *
import pyodbc
import time
import pandas as pd
import logging as log
from pandas import to_datetime

def timeit(func_to_decorate):
    """Decorator generator that logs the time it takes a function to execute"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func_to_decorate(*args, **kwargs)
        elapsed = ((time.time() - start) /60 )
        log.debug("[TIMING]: %s - %s minutos" % (func_to_decorate.__name__, elapsed))
        print("[TIMING]: %s - %s minutos" % (func_to_decorate.__name__, round(elapsed, 2)))
        print("*********************************  fin  ********************************")
        return result

    wrapper.__doc__ = func_to_decorate.__doc__
    wrapper.__name__ = func_to_decorate.__name__
    return wrapper



@timeit
def uploader_jp(dfmaster):
	"""ETL para cargar los Canales de venta, Direcciones,
	Coordinadores, Gerentes, Supervisores,Estados, Regiones, Locales"""


	#DF Jerarquia AA/ASI y CDS

	df = pd.read_excel(dfmaster, sheet_name='Inf Jerarquía Mensual')

	jq_cds = pd.read_excel(dfmaster, sheet_name='Inf Jerarquía CDS')


	#DF Homologadores
	df_plan = pd.read_excel(dfmaster, sheet_name='Inf Homologador de Planes')

	#DF Direcciones AA/ASI CDS
	direc=df.loc[:,'Dirección'].unique()
	direccds = jq_cds.loc[:,'Dirección'].unique()

	#DF Estados AA/ASI CDS
	edo=df.loc[:,'Estado'].unique()
	edocds=jq_cds.loc[:,'Estado'].unique()

	#DF Direcciones AA/ASI CDS
	reg=df.loc[:,'Región'].unique()
	regcds=jq_cds.loc[:,'Región'].unique()

	#DF Coordinadores AA/ASI
	coord=df.loc[:,'Coordinador'].unique()

	#DF Supervisores
	sup=df.loc[:,'Supervisor'].unique()


	#DF Gerentes AA/ASI CDS
	gte=df.loc[:,'Gerente'].unique()
	gtecds=jq_cds.loc[:,'Gerente'].unique()


	#DF Jerarquia
	jq=df.loc[:,('Año','Mes','Gerente','Coordinador','Supervisor')] #jq = jerarquia



	ubi=df.loc[:,('Región','Dirección','Estado')]
	ubicds=jq_cds.loc[:,('Región','Dirección','Estado')]



	#Obteniendo la fecha de las jerarquias (Aplica para ASI-AA y CDS)
	mes=jq.loc[0,'Mes']
	ano=jq.loc[0,'Año']
	fecha='%s-%s-01'%(ano,mes)
	print (fecha)


	#DF Master_Planes
	f_plan = pd.read_excel(dfmaster, sheet_name='Inf Homologador de Planes')

	#DF Homologadores
	homo_df = df_plan.loc[:,'Homologador de Planes'].unique()

	#DF Planes
	planes_df = df_plan.loc[:,('Código Plan','Nombre de Plan')]




	#Cargando las Direcciones ASI-AA
	for i in direc:
		try:
			Direccion.objects.get(nombre_dir__iexact=i)


		except Direccion.DoesNotExist:
			Direccion(nombre_dir=i).save()
			continue

	
	#Cargando las Direcciones CD
	for i in direccds:
		try:
			Direccion.objects.get(nombre_dir__iexact=i)



		except Direccion.DoesNotExist:
			Direccion(nombre_dir=i).save()
			continue



	#Cargando los Estados ASI-AA
	for i in edo:
		try:
			Estado.objects.get(estado__iexact=i)



		except Estado.DoesNotExist:
			Estado(estado=i).save()
			continue




	#Cargando los Estados CDS
	for i in edocds:
		try:
			Estado.objects.get(estado__iexact=i)

		except Estado.DoesNotExist:
			Estado(estado=i).save()
			continue



	#Carando las Regiones ASI-AA
	for i in reg:
		try:
			Region.objects.get(region__iexact=i)
			continue



		except Region.DoesNotExist:
			Region(region=i).save()
			continue




	#Carando las Regiones CDS
	for i in regcds:
		try:
			Region.objects.get(region__iexact=i)


		except Region.DoesNotExist:
			Region(region=i).save()
			continue




	#Cargando los Supervisores ASI-AA
	Supervisor.objects.exclude(nombre_super__startswith='DESJERARQUIZADO').update(activo=False)
	for i in sup:
		try:
			Supervisor.objects.get(nombre_super__iexact=i)
			Supervisor.objects.filter(nombre_super__iexact=i).update(activo=True)
			continue


		except Supervisor.DoesNotExist:
			Supervisor(nombre_super=i,activo=True).save()
			continue



	#Cargando los Coordinadores (Lideres) ASI-AA
	Coordinador.objects.exclude(nombre_coord__startswith='DESJERARQUIZADO').update(activo=False)
	for i in coord:
		try:
			Coordinador.objects.get(nombre_coord__iexact=i)
			Coordinador.objects.filter(nombre_coord__iexact=i).update(activo=True)
			continue

		except Coordinador.DoesNotExist:
			Coordinador(nombre_coord=i,activo=True).save()
			continue



	#Cargando los Gerentes ASI-AA
	Gerente.objects.exclude(nombre_gte__startswith='DESJERARQUIZADO').update(activo=False)
	for i in gte:
		try:
			Gerente.objects.get(nombre_gte__iexact=i)
			Gerente.objects.filter(nombre_gte__iexact=i).update(activo=True)
			continue

		except Gerente.DoesNotExist:
			Gerente(nombre_gte=i,activo=True).save()
			continue



	#Cargando los Gerentes CDS
	for i in gtecds:
		try:
			Gerente.objects.get(nombre_gte__iexact=i)
			Gerente.objects.filter(nombre_gte__iexact=i).update(activo=True) #Si lo encuentra en el excel, lo activa
			continue


		except Gerente.DoesNotExist:
			Gerente(nombre_gte=i,activo=True).save() #Si no existe, lo crea y lo activa
			continue








	#Apagando campos de Jerarquia, excepto combinacion DESJERARQUIZADO
	Jerarquia.objects.exclude(coordinador_key__nombre_coord="DESJERARQUIZADO",
		gerente_key__nombre_gte="DESJERARQUIZADO",
		supervisor_key__nombre_super="DESJERARQUIZADO").update(activo=False)





	#ASI-AA
	for fil,col in jq.iterrows():
		q=Jerarquia.objects.filter(
			gerente_key=Gerente.objects.get(nombre_gte__iexact=col['Gerente']),
		 	coordinador_key=Coordinador.objects.get(nombre_coord__iexact=col['Coordinador']),
		 	supervisor_key=Supervisor.objects.get(nombre_super__iexact=col['Supervisor']))


		if q.exists():
			q.update(activo=True)
			continue

		else:
			Jerarquia(gerente_key=Gerente.objects.get(nombre_gte__iexact=col['Gerente']),
		 	coordinador_key=Coordinador.objects.get(nombre_coord__iexact=col['Coordinador']),
		 	supervisor_key=Supervisor.objects.get(nombre_super__iexact=col['Supervisor']),
		 	activo=True).save()
			continue


	#CDS
	for fil,col in jq_cds.iterrows():
		q=Jerarquia.objects.filter(gerente_key=Gerente.objects.get(nombre_gte__iexact=col['Gerente']),
			coordinador_key__nombre_coord__iexact=None,
			supervisor_key__nombre_super__iexact=None)

		if q.exists():
			q.update(activo=True)
			continue

		else:
			Jerarquia(gerente_key=Gerente.objects.get(nombre_gte__iexact=col['Gerente']),
			activo=True).save()
			continue





	#Cargando Ubicacion de ASI-AA
	for fil,col in ubi.iterrows():


		q=Ubicacion.objects.filter(
			direccion_key=Direccion.objects.get(nombre_dir__iexact=col['Dirección']),
			region_key=Region.objects.get(region__iexact=col['Región']),
			estado_key=Estado.objects.get(estado__iexact=col['Estado']))

		if q.exists()==False:
			Ubicacion(
			direccion_key=Direccion.objects.get(nombre_dir__iexact=col['Dirección']),
			region_key=Region.objects.get(region__iexact=col['Región']),
			estado_key=Estado.objects.get(estado__iexact=col['Estado']) ).save()
			continue




	#Cargando Ubicacion de CDS
	for fil,col in ubicds.iterrows():



		q=Ubicacion.objects.filter(
			direccion_key=Direccion.objects.get(nombre_dir__iexact=col['Dirección']),
			region_key=Region.objects.get(region__iexact=col['Región']),
			estado_key=Estado.objects.get(estado__iexact=col['Estado']) )

		if q.exists()==False:
			Ubicacion(
			direccion_key=Direccion.objects.get(nombre_dir__iexact=col['Dirección']),
			region_key=Region.objects.get(region__iexact=col['Región']),
			estado_key=Estado.objects.get(estado__iexact=col['Estado']) ).save()
			continue






	#Cargando los Locales ASI-AA
	Local.objects.all().update(activo=False)

	for fil,col in df.iterrows():

		local=Local.objects.filter(codigo__iexact=col['Código Agente'])

		objjq = Jerarquia.objects.get(gerente_key__nombre_gte__iexact=col['Gerente'],
				coordinador_key__nombre_coord__iexact=col['Coordinador'],
				supervisor_key__nombre_super__iexact=col['Supervisor'],
				activo=True)

		objubi = Ubicacion.objects.get(estado_key__estado__iexact=col['Estado'],
			region_key__region__iexact=col['Región'],
			direccion_key__nombre_dir__iexact=col['Dirección'])





		if local.exists():

			local.update(nombre_local=col['AA'],
				codigo_sap=col['Código Sap'],
				direccion_fisica=col['Dirección AA'],
				cc=col['Ubicación CC / No CC'],
				jerarquia=objjq,
				canal=col['Canal'],
				ubicacion=objubi,activo=True)
			continue

		else:
			Local(codigo=col['Código Agente'],
				nombre_local=col['AA'],
				codigo_sap=col['Código Sap'],
				direccion_fisica=col['Dirección AA'],
				cc=col['Ubicación CC / No CC'],
				canal=col['Canal'],
				jerarquia=objjq,
				ubicacion=objubi,
				activo=True).save()




	#Cargando Locales CDS
	for fil,col in jq_cds.iterrows():

		local = Local.objects.filter(codigo__iexact=col['Nombre CDS'])


		objjq = Jerarquia.objects.get(gerente_key__nombre_gte__iexact=col['Gerente'],
			coordinador_key__nombre_coord__iexact=None,
			supervisor_key__nombre_super__iexact=None,
			activo=True)

		objubi=Ubicacion.objects.get(estado_key__estado__iexact=col['Estado'],
			region_key__region__iexact=col['Región'],
			direccion_key__nombre_dir__iexact=col['Dirección'])



		if local.exists():
			local.update(nombre_local=col['Nombre CDS'],
				cc=col['Ubicación CC / No CC'],
				jerarquia=objjq,
				ubicacion=objubi,
				activo=True)

		else:
			Local(codigo=col['Nombre CDS'],
			nombre_local=col['Nombre CDS'],
			cc=col['Ubicación CC / No CC'],
			canal='CDS',
			jerarquia=objjq,
			ubicacion=objubi,
			activo=True).save()


	des_j=Jerarquia.objects.get(
		coordinador_key=Coordinador.objects.get(nombre_coord__iexact='DESJERARQUIZADO'),
		gerente_key=Gerente.objects.get(nombre_gte__iexact='DESJERARQUIZADO'),
		supervisor_key=Supervisor.objects.get(nombre_super__iexact='DESJERARQUIZADO'))


	des_ubi=Ubicacion.objects.get(
		direccion_key=Direccion.objects.get(nombre_dir__iexact='DESJERARQUIZADO'),
		estado_key=Estado.objects.get(estado__iexact='DESJERARQUIZADO'),
		region_key=Region.objects.get(region__iexact='DESJERARQUIZADO'))

	Local.objects.filter(activo=False).update(jerarquia=des_j,ubicacion=des_ubi)






	#Cargando los Homologadores
	for i in homo_df:
		try:
			Homologador.objects.get(homologador__iexact=i)
			continue
		except Homologador.DoesNotExist:
			Homologador(homologador=i).save()
			continue


	#Cargando Planes
	for fil,col in planes_df.iterrows():
		try:
			Plan.objects.get(codigo_plan__iexact=col['Código Plan'])
			Plan.objects.filter(codigo_plan__iexact=col['Código Plan']).update(
				nombre_plan=col['Nombre de Plan'])
			continue

		except Plan.DoesNotExist:
			Plan(codigo_plan=col['Código Plan'],
				nombre_plan=col['Nombre de Plan']).save()
			continue


	

	mes=df_plan.loc[0,'Mes']
	ano=df_plan.loc[0,'Año']
	fecha_prod='%s-%s-01'%(ano,mes)


	
	ProduccionPlan.objects.filter(fecha_prod__year=ano,fecha_prod__month=mes).delete()


	for fil,col in df_plan.iterrows():
		ProduccionPlan(fecha_prod=fecha_prod,
		homologador=Homologador.objects.get(homologador__iexact=col['Homologador de Planes']),
		plan=Plan.objects.get(codigo_plan__iexact=col['Código Plan']),
		renta_mensual=col['Renta Mensual por Plan'],
		recarga_plan=col['Recarga por Plan']).save()

		continue


	#Sincronizando los Homologadores de la Historia que no esten en los Homologadores actuales
	p = ProduccionPlan.objects.exclude(homologador__homologador__in = homo_df)
	p.update(homologador=Homologador.objects.get(homologador__iexact='Otros Planes'))

	return
