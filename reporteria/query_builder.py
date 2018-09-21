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



def premisas(datos,select_interno, select_externo, group_interno, group_externo,actividad):
	"""Ajusta el query en funcion a ciertas premisas que existen por las combinaciones"""

	"""Inserta en el select interno los operandos de la multiplicacion que hace Renta Total
	o Recarga Total en el select externo"""

	if (actividad == 'activacion') or (actividad == 'alta'):

		if ("Recarga Total" in datos) or ("Renta Total" in datos):


			if "SUM(A.CANTIDAD) AS CANTIDAD" not in select_interno:
				select_interno.append('SUM(A.CANTIDAD) AS CANTIDAD')


			if 'Renta Total' in datos:
				if "PP.RENTA_MENSUAL AS RENTA_MENSUAL" not in select_interno:
					select_interno.append('PP.RENTA_MENSUAL AS RENTA_MENSUAL')
					group_interno.append('PP.RENTA_MENSUAL')

			if 'Recarga Total' in datos:
				if "PP.RECARGA_PLAN AS RECARGA_PLAN" not in select_interno:
					select_interno.append('PP.RECARGA_PLAN AS RECARGA_PLAN')
					group_interno.append('PP.RECARGA_PLAN')

	else: #Actividad es Bajas

		if ("Recarga Total" in datos) or ("Renta Total" in datos):

			if "SUM(A.BRUTA) AS BRUTAS" not in select_interno:
				select_interno.append('SUM(A.BRUTA) AS BRUTAS')

			if "SUM(A.REACTIVADA) AS REACTIVADAS" not in select_interno:
				select_interno.append('SUM(A.REACTIVADA) AS REACTIVADAS')

			if "SUM(A.NETA) AS NETAS" not in select_interno:
				select_interno.append('SUM(A.NETA) AS NETAS')



			if 'Renta Total' in datos:
				if "PP.RENTA_MENSUAL AS RENTA_MENSUAL" not in select_interno:
					select_interno.append('PP.RENTA_MENSUAL AS RENTA_MENSUAL')
					group_interno.append('PP.RENTA_MENSUAL')


			if 'Recarga Total' in datos:
				if "PP.RECARGA_PLAN AS RECARGA_PLAN" not in select_interno:
					select_interno.append('PP.RECARGA_PLAN AS RECARGA_PLAN')
					group_interno.append('PP.RECARGA_PLAN')


	return









def query_builder(fechas,actividad,datos):

	engine = create_engine("mssql+pyodbc://sa:BaseSQL123@10.160.8.96:1433/vpcanales?driver=SQL+Server+Native+Client+11.0")
	select_interno=[]
	select_externo=[]

	from_interno=[]
	from_externo=[]

	group_interno=[]
	group_externo=[]

# SELECT SECTION

	# Date Variables

	if 'Dia' in datos:
		select_interno.append('a.fecha_actividad as FECHA')
		select_interno.append('DATENAME(DW, a.fecha_actividad) as WEEKDAY ')
		group_interno.append('a.fecha_actividad')
		group_interno.append('DATENAME(DW, a.fecha_actividad)')

		select_externo.append("TABLA.FECHA AS FECHA")
		select_externo.append("TABLA.WEEKDAY AS 'NOMBRE DE DIA'")
		group_externo.append("TABLA.FECHA")
		group_externo.append("TABLA.WEEKDAY")

	if 'Semana' in datos:
		select_interno.append("CONCAT (DATEPART(WEEK,A.FECHA_ACTIVIDAD),'_',(DATEPART(YEAR,A.FECHA_ACTIVIDAD))) AS SEMANA")
		group_interno.append("CONCAT (DATEPART(WEEK,A.FECHA_ACTIVIDAD),'_',(DATEPART(YEAR,A.FECHA_ACTIVIDAD)))")

		select_externo.append("TABLA.SEMANA AS SEMANA")
		group_externo.append("TABLA.SEMANA")


	if 'Mes' in datos:
		select_interno.append("CONCAT (DATEPART(MONTH,A.FECHA_ACTIVIDAD),'_',(DATEPART(YEAR,A.FECHA_ACTIVIDAD))) AS MES")
		group_interno.append("CONCAT (DATEPART(MONTH,A.FECHA_ACTIVIDAD),'_',(DATEPART(YEAR,A.FECHA_ACTIVIDAD)))")

		select_externo.append("TABLA.MES AS MES")
		group_externo.append("TABLA.MES")

	if 'Trimestre' in datos:
		select_interno.append("CONCAT (DATEPART(QUARTER,A.FECHA_ACTIVIDAD),'_' ,DATEPART(YEAR,A.FECHA_ACTIVIDAD)) AS Q")
		group_interno.append("CONCAT (DATEPART(QUARTER,A.FECHA_ACTIVIDAD),'_' ,DATEPART(YEAR,A.FECHA_ACTIVIDAD))")

		select_externo.append("TABLA.Q AS TRIMESTRE")
		group_externo.append("TABLA.Q")

	if 'Semestre' in datos:
		select_interno.append("CONCAT((CASE WHEN DATEPART(MONTH, A.FECHA_ACTIVIDAD) BETWEEN 1 AND 6 THEN 'I' WHEN DATEPART(MONTH, A.FECHA_ACTIVIDAD) BETWEEN 7 AND 12 THEN 'II' END) , '_',DATEPART(YEAR,A.FECHA_ACTIVIDAD))  AS SEMESTRE")
		group_interno.append("CONCAT((CASE WHEN DATEPART(MONTH, A.FECHA_ACTIVIDAD) BETWEEN 1 AND 6 THEN 'I' WHEN DATEPART(MONTH, A.FECHA_ACTIVIDAD) BETWEEN 7 AND 12 THEN 'II' END) , '_',DATEPART(YEAR,A.FECHA_ACTIVIDAD))")

		select_externo.append("TABLA.SEMESTRE AS SEMESTRE")
		group_externo.append("TABLA.SEMESTRE")

	if 'Ano' in datos:
		select_interno.append("DATEPART(YEAR,A.FECHA_ACTIVIDAD) AS AÑO")
		group_interno.append("DATEPART(YEAR,A.FECHA_ACTIVIDAD)")

		select_externo.append("TABLA.AÑO AS AÑO")
		group_externo.append("TABLA.AÑO")


	# Agents Variables

	if 'Codigo de Agente' in datos:
		select_interno.append("L.CODIGO AS CODIGO_AGENTE")
		group_interno.append("L.CODIGO")

		select_externo.append("TABLA.CODIGO_AGENTE AS 'CODIGO DE AGENTE'")
		group_externo.append("TABLA.CODIGO_AGENTE")

	if 'Codigo SAP' in datos:
		select_interno.append("L.CODIGO_SAP AS CODIGO_SAP")
		group_interno.append("L.CODIGO_SAP")

		select_externo.append("TABLA.CODIGO_SAP AS 'CODIGO SAP'")
		group_externo.append("TABLA.CODIGO_SAP")


	if 'Nombre de Agente' in datos:
		select_interno.append('L.NOMBRE_LOCAL AS NOMBRE_LOCAL')
		group_interno.append('L.NOMBRE_LOCAL')

		select_externo.append("TABLA.NOMBRE_LOCAL AS 'NOMBRE DEL AGENTE'")
		group_externo.append("TABLA.NOMBRE_LOCAL")


	if 'Centro Comercial' in datos:
		select_interno.append('L.CC AS CC')
		group_interno.append('L.CC')

		select_externo.append("TABLA.CC AS 'CENTRO COMERCIAL'")
		group_externo.append("TABLA.CC")


	if 'Estado' in datos:
		select_interno.append('E.ESTADO AS ESTADO')
		group_interno.append('E.ESTADO')

		select_externo.append("TABLA.ESTADO AS ESTADO")
		group_externo.append("TABLA.ESTADO")


	if 'Region' in datos:
		select_interno.append('R.REGION AS REGION')
		group_interno.append('R.REGION')

		select_externo.append("TABLA.REGION AS REGION")
		group_externo.append("TABLA.REGION")


	if 'Este/Oeste' in datos:
		select_interno.append("D.NOMBRE_DIR AS DIRECCION")
		group_interno.append("D.NOMBRE_DIR")

		select_externo.append("TABLA.DIRECCION AS DIRECCION")
		group_externo.append("TABLA.DIRECCION")


	if 'Direccion fisica' in datos:
		select_interno.append('L.DIRECCION_FISICA AS DIRECCION_FISICA')
		group_interno.append('L.DIRECCION_FISICA')

		select_externo.append("TABLA.DIRECCION_FISICA AS 'DIRECCION FISICA'")
		group_externo.append("TABLA.DIRECCION_FISICA")



	if 'Canal de Venta' in datos:
		select_interno.append('L.CANAL AS CANAL')
		group_interno.append('L.CANAL')

		select_externo.append("TABLA.CANAL AS 'CANAL DE VENTA'")
		group_externo.append("TABLA.CANAL")


	# Others Variables

	if 'Gerente' in datos:
		select_interno.append('G.NOMBRE_GTE AS GERENTE')
		group_interno.append('G.NOMBRE_GTE')

		select_externo.append("TABLA.GERENTE AS GERENTE")
		group_externo.append("TABLA.GERENTE")


	if 'Lider' in datos:
		select_interno.append('S.NOMBRE_SUPER AS LIDER')
		group_interno.append('S.NOMBRE_SUPER')

		select_externo.append("TABLA.LIDER AS LIDER")
		group_externo.append("TABLA.LIDER")


	if 'Coordinador' in datos:
		select_interno.append('C.NOMBRE_COORD AS COORDINADOR')
		group_interno.append('C.NOMBRE_COORD')

		select_externo.append("TABLA.COORDINADOR AS COORDINADOR")
		group_externo.append("TABLA.COORDINADOR")


	if 'Terminal' in datos:
		select_interno.append('A.TERMINAL AS TERMINAL')
		group_interno.append('A.TERMINAL')

		select_externo.append("TABLA.TERMINAL AS 'TIPO TERMINAL'")
		group_externo.append("TABLA.TERMINAL")


	if 'Tecnologia' in datos:
		select_interno.append('A.TECNOLOGIA AS TECNOLOGIA')
		group_interno.append('A.TECNOLOGIA')

		select_externo.append("TABLA.TECNOLOGIA AS TECNOLOGIA")
		group_externo.append("TABLA.TECNOLOGIA")

	if 'Plataforma' in datos:
		select_interno.append('A.PLATAFORMA AS PLATAFORMA')
		group_interno.append('A.PLATAFORMA')

		select_externo.append("TABLA.PLATAFORMA AS PLATAFORMA")
		group_externo.append("TABLA.PLATAFORMA")


	# Plan Variables

	if 'Codigo Plan' in datos:
		select_interno.append('P.CODIGO_PLAN AS CODIGO_PLAN')
		group_interno.append('P.CODIGO_PLAN')

		select_externo.append("TABLA.CODIGO_PLAN AS 'CODIGO DE PLAN'")
		group_externo.append("TABLA.CODIGO_PLAN")

	if 'Nombre Plan' in datos:
		select_interno.append('H.HOMOLOGADOR AS NOMBRE_PLAN')
		group_interno.append('H.HOMOLOGADOR')

		select_externo.append("TABLA.NOMBRE_PLAN AS 'NOMBRE DE PLAN'")
		group_externo.append("TABLA.NOMBRE_PLAN")

	if 'Renta Mensual' in datos:
		select_interno.append('PP.RENTA_MENSUAL AS RENTA_MENSUAL')
		group_interno.append('PP.RENTA_MENSUAL')

		select_externo.append("TABLA.RENTA_MENSUAL AS 'RENTA MENSUAL'")
		group_externo.append("TABLA.RENTA_MENSUAL")

	if 'Recarga Mensual' in datos:
		select_interno.append('PP.RECARGA_PLAN AS RECARGA_PLAN')
		group_interno.append('PP.RECARGA_PLAN')

		select_externo.append("TABLA.RECARGA_PLAN AS 'RECARGA POR PLAN'")
		group_externo.append("TABLA.RECARGA_PLAN")





	if (actividad == 'activacion') or (actividad == 'alta'):

		if 'Cantidad' in datos:
			select_interno.append('SUM(A.CANTIDAD) AS CANTIDAD')
			select_externo.append("SUM(TABLA.CANTIDAD) AS CANTIDAD")

		if 'Renta Total' in datos:
			select_externo.append("SUM(TABLA.CANTIDAD * TABLA.RENTA_MENSUAL) AS 'RENTA TOTAL'")

		if 'Recarga Total' in datos:
			select_externo.append("SUM(TABLA.CANTIDAD * TABLA.RECARGA_PLAN) AS 'RECARGA TOTAL'")

	else:

		if 'Bajas Brutas' in datos:
			select_interno.append('SUM(A.BRUTA) AS BRUTAS')
			select_externo.append("SUM(TABLA.BRUTAS) AS 'BAJAS BRUTAS' ")

		if 'Bajas Reactivada' in datos:
			select_interno.append('SUM(A.REACTIVADA) AS REACTIVADAS')
			select_externo.append("SUM(TABLA.REACTIVADAS) AS REACTIVADAS")

		if 'Bajas Neta' in datos:
			select_interno.append('SUM(A.NETA) AS NETAS')
			select_externo.append("SUM(TABLA.NETAS) AS 'BAJAS NETAS' ")



		if 'Renta Total' in datos:
			select_externo.append("SUM(TABLA.BRUTAS * TABLA.RENTA_MENSUAL) AS 'RENTA TOTAL BRUTA'")

		if 'Renta Total' in datos:
			select_externo.append("SUM(TABLA.REACTIVADAS * TABLA.RENTA_MENSUAL) AS 'RENTA TOTAL REACTIVADA'")

		if 'Renta Total' in datos:
			select_externo.append("SUM(TABLA.NETAS * TABLA.RENTA_MENSUAL) AS 'RENTA TOTAL NETA'")





		if 'Recarga Total' in datos:
			select_externo.append("SUM(TABLA.BRUTAS * TABLA.RECARGA_PLAN) AS 'RECARGA TOTAL BRUTA'")

		if 'Recarga Total' in datos:
			select_externo.append("SUM(TABLA.REACTIVADAS * TABLA.RECARGA_PLAN) AS 'RECARGA TOTAL REACTIVADA'")

		if 'Recarga Total' in datos:
			select_externo.append("SUM(TABLA.NETAS * TABLA.RECARGA_PLAN) AS 'RECARGA TOTAL NETA'")








	# Se ajusta el subquery para Recarga Total y Renta Total
	premisas(datos,select_interno, select_externo, group_interno, group_externo,actividad)





# FROM SECTION

	if ('Renta Mensual' in datos) or ('Recarga Mensual' in datos) or \
	('Renta Total' in datos) or ('Recarga Total' in datos):
		from_interno.append("INNER JOIN REPORTERIA_PRODUCCIONPLAN PP ON PP.ID = A.PLAN_KEY_ID")



	# Si solicitan nombre_plan o codigo_plan pero
	# no esta joinneada Produccion Plan, hay que agregar REPORTERIA_PRODUCCIONPLAN
	if (('Nombre Plan' in datos) or ('Codigo Plan' in datos)) and \
	("INNER JOIN REPORTERIA_PRODUCCIONPLAN PP ON PP.ID = A.PLAN_KEY_ID" not in from_interno):
		from_interno.append("INNER JOIN REPORTERIA_PRODUCCIONPLAN PP ON PP.ID = A.PLAN_KEY_ID")

		if 'Nombre Plan' in datos:
			from_interno.append("INNER JOIN REPORTERIA_HOMOLOGADOR H ON H.ID = PP.HOMOLOGADOR_ID")

		if 'Codigo Plan' in datos:
			from_interno.append("INNER JOIN REPORTERIA_PLAN P ON  P.ID = PP.PLAN_ID")

	else:
		if 'Nombre Plan' in datos:
			from_interno.append("INNER JOIN REPORTERIA_HOMOLOGADOR H ON H.ID = PP.HOMOLOGADOR_ID")

		if 'Codigo Plan' in datos:
			from_interno.append("INNER JOIN REPORTERIA_PLAN P ON  P.ID = PP.PLAN_ID")




	if ('Codigo de Agente' in datos) or ('Codigo SAP' in datos) or \
	('Nombre de Agente' in datos) or ('Centro Comercial' in datos) or \
	('Direccion fisica' in datos) or ('Canal de Venta' in datos):
		from_interno.append("INNER JOIN REPORTERIA_LOCAL L ON L.ID = A.LOCAL_KEY_ID")







	if 	('Gerente' in datos) or ('Lider' in datos) or ('Coordinador' in datos):

		if ("INNER JOIN REPORTERIA_LOCAL L ON L.ID = A.LOCAL_KEY_ID" not in from_interno):
			from_interno.append("INNER JOIN REPORTERIA_LOCAL L ON L.ID = A.LOCAL_KEY_ID")

		from_interno.append("INNER JOIN REPORTERIA_JERARQUIA J ON J.ID = L.JERARQUIA_ID")


		if 'Gerente' in datos:
			from_interno.append("INNER JOIN REPORTERIA_GERENTE G ON G.ID = J.GERENTE_KEY_ID ")

		if 'Lider' in datos:
			from_interno.append("LEFT JOIN REPORTERIA_SUPERVISOR S ON S.ID = J.SUPERVISOR_KEY_ID")

		if 'Coordinador' in datos:
			from_interno.append("LEFT JOIN REPORTERIA_COORDINADOR C ON C.ID = J.COORDINADOR_KEY_ID")











	if ('Estado' in datos) or ('Region' in datos) or ('Este/Oeste' in datos):

		if ('INNER JOIN REPORTERIA_LOCAL L ON L.ID = A.LOCAL_KEY_ID' not in from_interno):
			from_interno.append("INNER JOIN REPORTERIA_LOCAL L ON L.ID = A.LOCAL_KEY_ID")

		from_interno.append("INNER JOIN REPORTERIA_UBICACION U ON U.ID = L.UBICACION_ID")


		if 'Estado' in datos:
			from_interno.append("INNER JOIN REPORTERIA_ESTADO E ON E.ID = U.ESTADO_KEY_ID")

		if 'Region' in datos:
			from_interno.append("INNER JOIN REPORTERIA_REGION R ON R.ID = U.REGION_KEY_ID")

		if 'Este/Oeste' in datos:
			from_interno.append("INNER JOIN REPORTERIA_DIRECCION D ON D.ID = U.DIRECCION_KEY_ID")










# BUILDING INTERNAL QUERY
	subquery = "SELECT "

	for i in select_interno:
		if i == select_interno[-1]:
			subquery = subquery + i + '\n'
		else:
			subquery = subquery + i + ' , \n'

	subquery = subquery + '\n \nFROM REPORTERIA_'+actividad+' A \n '

	for i in from_interno:
		subquery = subquery + i + '\n'


	subquery = subquery + "\n \nWHERE A.FECHA_ACTIVIDAD BETWEEN '%s' AND  '%s' \n \n"%(fechas[0],fechas[1])

	subquery = subquery + "GROUP BY "

	for i in group_interno:
		if i == group_interno[-1]:
			subquery = subquery + i + '\n'
		else:
			subquery = subquery + i + ' , \n'






	query = "SELECT "

	for i in select_externo:
		if i == select_externo[-1]:
			query = query + i + '\n'
		else:
			query = query + i + ', \n '

	query = query + "FROM \n ( %s ) as TABLA  \n GROUP BY "%(subquery)

	for i in group_externo:
		if i == group_externo[-1]:
			query = query + i + '\n'
		else:
			query = query + i + ' , \n'

	print("El query generado es: \n\n" , query , "\n\n ********************************")
	q=pd.read_sql_query(query, engine)



	print(q)

	return q
