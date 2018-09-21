from django.shortcuts import render
from .models import *
import pyodbc
import time
from datetime import datetime, date
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging as log
from pandas import to_datetime
from django.db.models import  Count, Sum



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
def uploader_actividad(df,to_model):
	"""Proceso ETL para las Activaciones o ALtas"""
	engine = create_engine("mssql+pyodbc://sa:BaseSQL123@10.160.8.96:1433/vpcanales?driver=SQL+Server+Native+Client+11.0")

	fecha = df.loc[0,'Fecha']
	print(fecha.month)
	print(fecha.year)

	if to_model.__name__=="Activacion":

		Activacion.objects.filter(fecha_actividad__month=fecha.month ,
			fecha_actividad__year=fecha.year).delete()

		for row in df.itertuples():
			connection = engine.raw_connection()
			cursor=connection.cursor()
			#Se ejecuta el SP por cada registro del dataframe
			string="""exec sp_insert_into_activacion
			@fecha_actividad='{0}',
			@plataforma='{1}',
			@tecnologia='{2}',
			@terminal='{3}',
			@cantidad='{4}',
			@codigo_plan='{5}',
			@mes={6},
			@ano={7},
			@codigo_agente='{8}'
			 """.format(row[2],
			row[5],
			row[6],
			row[7],
			row[-2],
			row[4],
			row[2].month,
			row[2].year,
			row[3])
			cursor.execute(string).commit()

		results = Activacion.objects.filter(fecha_actividad__month=fecha.month,\
			fecha_actividad__year=fecha.year)\
			.aggregate(suma = Sum('cantidad'))


		results.update(Activacion.objects.filter(fecha_actividad__month=fecha.month,\
			fecha_actividad__year=fecha.year)\
			.aggregate(count = Count('cantidad')))

		print("*************************",results)

		return results



	else:

		Alta.objects.filter(fecha_actividad__month=fecha.month ,
			fecha_actividad__year=fecha.year).delete()

		for row in df.itertuples():
			connection = engine.raw_connection()
			cursor=connection.cursor()
			#Se ejecuta el SP por cada registro del dataframe
			string="""exec sp_insert_into_alta
	        @fecha_actividad='{0}',
	        @plataforma='{1}',
	        @tecnologia='{2}',
	        @terminal='{3}',
	        @cantidad='{4}',
	        @codigo_plan='{5}',
	        @mes={6},
	        @ano={7},
	        @codigo_agente='{8}' """.format(row[2],
	        row[5],
	        row[6],
	        row[7],
	        row[-2],
	        row[4],
	        row[2].month,
	        row[2].year,
	        row[3])
			cursor.execute(string).commit()


		results = Alta.objects.filter(fecha_actividad__month=fecha.month,\
			fecha_actividad__year=fecha.year)\
			.aggregate(suma = Sum('cantidad'))


		results.update(Alta.objects.filter(fecha_actividad__month=fecha.month,\
			fecha_actividad__year=fecha.year)\
			.aggregate(count = Count('cantidad')))

		print("*************************",results)



		return results
