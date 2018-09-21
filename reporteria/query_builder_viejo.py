import pandas as pd
from sqlalchemy import create_engine
from django.contrib import messages
import os
from pandas.io import sql
import pyodbc
from sqlalchemy import create_engine
from time import time
from django.http import HttpResponse
from xlsxwriter.workbook import Workbook


def query_builder(fechas,actividad,datos):

	engine = create_engine("mssql+pyodbc://sa:BaseSQL123@10.160.8.162:1433/vpcanales?driver=SQL+Server+Native+Client+11.0")
	total=[]
	select=[]
	groupby=[]
	pandasgroup=[]

	if 'Renta Total' in datos:
		total.append('renta_total')

	if 'Recarga Total' in datos:
		total.append('recarga_total')

	if 'Dia' in datos:
		select.append('a.fecha_actividad')

		select.append('DATENAME(DW, a.fecha_actividad) as weekday')
		groupby.append('DATENAME(DW, a.fecha_actividad)')
		pandasgroup.append('weekday')
		pandasgroup.append('fecha_actividad')

	if 'Semana' in datos:
		select.append("CONCAT (DATEPART(week,a.fecha_actividad),'_',(DATEPART(year,a.fecha_actividad))) as Semana")
		groupby.append("CONCAT (DATEPART(week,a.fecha_actividad),'_',(DATEPART(year,a.fecha_actividad)))")
		pandasgroup.append('Semana')

	if 'Mes' in datos:
		select.append("CONCAT (DATEPART(month,a.fecha_actividad),'_',(DATEPART(year,a.fecha_actividad))) as Mes")
		groupby.append("CONCAT (DATEPART(month,a.fecha_actividad),'_',(DATEPART(year,a.fecha_actividad)))")
		pandasgroup.append('Mes')

	if 'Trimestre' in datos:
		select.append("CONCAT (DATEPART(quarter,a.fecha_actividad),'_' ,DATEPART(year,a.fecha_actividad)) AS Q")
		groupby.append("CONCAT (DATEPART(quarter,a.fecha_actividad),'_' ,DATEPART(year,a.fecha_actividad))")
		pandasgroup.append('Q')

	if 'Semestre' in datos:
		select.append("CONCAT((CASE WHEN DATEPART(MONTH, a.fecha_actividad) between 1 and 6 then 'I' WHEN DATEPART(MONTH, a.fecha_actividad) between 7 and 12 then 'II' end) , '_',DATEPART(year,a.fecha_actividad))  as Semestre")
		groupby.append("CONCAT((CASE WHEN DATEPART(MONTH, a.fecha_actividad) between 1 and 6 then 'I' WHEN DATEPART(MONTH, a.fecha_actividad) between 7 and 12 then 'II' end) , '_',DATEPART(year,a.fecha_actividad)) ")
		pandasgroup.append('Semestre')

	if 'Ano' in datos:
		select.append('DATEPART(year,a.fecha_actividad) as Año')
		groupby.append('DATEPART(year,a.fecha_actividad)')
		pandasgroup.append('Año')

	if 'Codigo de Agente' in datos:
		select.append('L.codigo')
		groupby.append('L.codigo')
		pandasgroup.append('codigo')

	if 'Codigo SAP' in datos:
		select.append('L.codigo_sap')
		groupby.append('L.codigo_sap')
		pandasgroup.append('codigo_sap')

	if 'Nombre de Agente' in datos:
		select.append('L.nombre_local')
		groupby.append('L.nombre_local')
		pandasgroup.append('nombre_local')

	if 'Centro Comercial' in datos:
		select.append('L.CC')
		groupby.append('L.CC')
		pandasgroup.append('CC')

	if 'Estado' in datos:
		select.append('E.estado')
		groupby.append('E.estado')
		pandasgroup.append('estado')

	if 'Region' in datos:
		select.append('R.region')
		groupby.append('R.region')
		pandasgroup.append('region')

	if 'Este/Oeste' in datos:
		select.append('D.nombre_dir')
		groupby.append('D.nombre_dir')
		pandasgroup.append('nombre_dir')

	if 'Canal de Venta' in datos:
		select.append('L.canal')
		groupby.append('L.canal')
		pandasgroup.append('canal')

	if 'Direccion fisica' in datos:
		select.append('L.direccion_fisica')
		groupby.append('L.direccion_fisica')
		pandasgroup.append('direccion_fisica')

	if 'Codigo Plan' in datos:
		select.append('p.codigo_plan')
		groupby.append('p.codigo_plan')
		pandasgroup.append('codigo_plan')


	if 'Nombre Plan' in datos:
		select.append('h.homologador')
		groupby.append('h.homologador')
		pandasgroup.append('homologador')

	if 'Renta Mensual' in datos:
		if 'renta_total' in total:
			select.append('pp.renta_mensual')
			groupby.append('pp.renta_mensual')
			# pandasgroup.append('renta_mensual')
		else:
			select.append('sum(pp.renta_mensual) as renta_mensual')
			groupby.append('pp.renta_mensual')
			# pandasgroup.append('renta_mensual')

	if 'Recarga Mensual' in datos:
		if 'recarga_total' in total:
			select.append('pp.recarga_plan')
			groupby.append('pp.recarga_plan')
			# pandasgroup.append('recarga_plan')
		else:
			select.append('sum(pp.recarga_plan) as recarga_plan')
			groupby.append('pp.recarga_plan')
			# pandasgroup.append('recarga_plan')

	if 'Cantidad' in datos:
		select.append('sum(a.cantidad) as Cantidad')
        # ARREGLAR LAS CONDICIONES SOBRE BAJAS
	if 'Bajas Brutas' in datos:
		select.append('sum(a.bruta) as Brutas')
	if 'Bajas Reactivada' in datos:
		select.append('sum(a.reactivada) as Reactivadas')
	if 'Bajas Neta' in datos:
		select.append('sum(a.neta) as Netas')

	if 'Gerente' in datos:
		select.append('G.nombre_gte')
		groupby.append('G.nombre_gte')
		pandasgroup.append('nombre_gte')

	if 'Lider' in datos:
		select.append('S.nombre_super')
		groupby.append('S.nombre_super')
		pandasgroup.append('nombre_super')

	if 'Coordinador' in datos:
		select.append('C.nombre_coord')
		groupby.append('C.nombre_coord')
		pandasgroup.append('nombre_coord')

	if 'Terminal' in datos:
		select.append('A.terminal')
		groupby.append('A.terminal')
		pandasgroup.append('terminal')

	if 'Tecnologia' in datos:
		select.append('a.tecnologia')
		groupby.append('a.tecnologia')
		pandasgroup.append('tecnologia')

	if 'Plataforma' in datos:
		select.append('a.plataforma')
		groupby.append('a.plataforma')
		pandasgroup.append('plataforma')

	if ('Renta Total' in datos) and (('Renta Mensual' in datos) == False):
		select.append('pp.renta_mensual')
		groupby.append('pp.renta_mensual')
		# pandasgroup.append('renta_mensual')

	if ('Recarga Total' in datos) and (('Recarga Mensual' in datos) == False):
		select.append('pp.recarga_plan')
		groupby.append('pp.recarga_plan')
		# pandasgroup.append('recarga_plan')



    # Despues de condicionar se arma el Query

	query = """select """
	if select:
		ultimo = select[-1]
	else:
		select.append('a.fecha_actividad')
		ultimo = select[-1]
	for items in select:
	    if items == ultimo:

	        query = query + items + ' '

	    else:
	        query = query + items + ', '

	query = query+'from reporteria_'+actividad+""" a INNER JOIN reporteria_local l on l.id = a.local_key_id
	INNER JOIN reporteria_jerarquia J ON J.ID = L.jerarquia_id
	INNER JOIN reporteria_gerente G ON G.id = J.gerente_key_id
	LEFT JOIN reporteria_supervisor S ON S.id = J.supervisor_key_id
	LEFT JOIN reporteria_coordinador C ON C.id = J.coordinador_key_id
	INNER JOIN reporteria_ubicacion U ON U.id = L.ubicacion_id
	INNER  JOIN reporteria_direccion D ON D.id = U.direccion_key_id
	INNER JOIN reporteria_estado E ON E.ID = U.estado_key_id
	INNER JOIN reporteria_region R ON R.ID = U.region_key_id
	INNER JOIN reporteria_produccionplan pp ON pp.id = a.plan_key_id
	INNER JOIN reporteria_homologador h ON h.id = pp.homologador_id
	INNER JOIN reporteria_plan p ON  p.id = pp.plan_id
	    where a.fecha_actividad between '%s' and  '%s'
	    """%(fechas[0],fechas[1])



	if groupby:
		query = query + ' group by a.fecha_actividad , '
		ultimo = groupby[-1]
		for items in groupby:
		    if items == ultimo:
		        query = query + items + ' '
		    else:
		        query = query + items + ', '

	query=query + " order by a.fecha_actividad desc"



	print(query)

	q=pd.read_sql_query(query, engine)
	


#HACER UNA FUNCION DE ESTO Y AGREGAR CONDICIONES DE BAJAS
	can_net = ''
	if 'Cantidad' in datos:
		can_net = 'Cantidad'
	if  'Bajas Neta' in datos:
		can_net = 'Netas'
	if ('renta_total' in total) and ('recarga_total' in total):
		if ('Recarga Mensual' in datos) and ('Renta Mensual' in datos):

			q['recarga_total']= q['recarga_plan'] * q[can_net]
			q['renta_total']= q['renta_mensual']*q[can_net]
			q.drop('recarga_plan', axis=1, inplace=True)
			q.drop('renta_mensual', axis=1, inplace=True)
			if not pandasgroup:
				q.groupby(can_net).sum()
			else:
				q= q.groupby(pandasgroup)[can_net,'renta_total','recarga_total'].sum()
			# q=q.reset_index(drop = True)
			q = q.reset_index()
		if ('Recarga Mensual' in datos) and ('Renta Mensual' in datos)==False:
			q['recarga_total']= q['recarga_plan'] * q[can_net]
			q['renta_total']= q['renta_mensual']*q[can_net]
			q.drop('recarga_plan', axis=1, inplace=True)
			q.drop('renta_mensual', axis=1, inplace=True)
			if not pandasgroup:
				q.groupby(can_net).sum()
			else:
				q= q.groupby(pandasgroup)[can_net,'renta_total','recarga_total'].sum()
			# q=q.reset_index(drop = True)
			q = q.reset_index()
		if ('Renta Mensual' in datos) and ('Recarga Mensual' in datos)==False:
			q['recarga_total']= q['recarga_plan'] * q[can_net]
			q['renta_total']= q['renta_mensual']*q[can_net]
			q.drop('recarga_plan', axis=1, inplace=True)
			q.drop('renta_mensual', axis=1, inplace=True)
			if not pandasgroup:
				q.groupby(can_net).sum()
			else:
				q= q.groupby(pandasgroup)[can_net,'renta_total','recarga_total'].sum()
			# q=q.reset_index(drop = True)
			q = q.reset_index()




	if ('renta_total' in total) and ('recarga_total' in total)==False:
		if 'Renta Mensual' in datos:
			q['renta_total']= q['renta_mensual']*q[can_net]
			q.drop('renta_mensual', axis=1, inplace=True)
			if not pandasgroup:
				q.groupby(can_net).sum()
			else:
					q= q.groupby(pandasgroup)[can_net,'renta_total'].sum()
			# q=q.reset_index(drop = True)
			q = q.reset_index()
		else:
			q['renta_total']= q['renta_mensual']*q[can_net]
			q.drop('renta_mensual',axis=1,inplace=True)
			if not pandasgroup:
				q.groupby(can_net).sum()
			else:
					q= q.groupby(pandasgroup)[can_net,'renta_total'].sum()
			# q=q.reset_index(drop = True)
			q = q.reset_index()


	if ('recarga_total' in total) and ('renta_total' in total)==False:
		if 'Recarga Mensual' in datos:
			q['recarga_total']= q['recarga_plan'] * q[can_net]
			q.drop('recarga_plan', axis=1, inplace=True)
			if not pandasgroup:
				q.groupby(can_net).sum()
			else:
				q=q.groupby(pandasgroup)[can_net,'recarga_total'].sum()
			# q=q.reset_index(drop = True)
			q = q.reset_index()
			print('entra',q)
		else:
			q['recarga_total']= q['recarga_plan'] * q[can_net]
			q.drop('recarga_plan',axis=1,inplace=True)
			if not pandasgroup:
				q.groupby(can_net).sum()
			else:
				q=q.groupby(pandasgroup)[can_net,'recarga_total'].sum()
			# q=q.reset_index(drop = True)
			q = q.reset_index()

	print (q)


	return q
