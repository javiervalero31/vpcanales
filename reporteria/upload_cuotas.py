from django.shortcuts import render
from .models import *
import pyodbc
import time
from datetime import datetime, date
import pandas as pd
from sqlalchemy import create_engine
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
def uploader_cuotas(df):
	"""ETL encargado de cargar la informacion de Cuotas"""
	engine = create_engine("mssql+pyodbc://sa:BaseSQL123@10.160.8.96:1433/VPCANALES?driver=SQL+Server+Native+Client+11.0")
	fecha_cuota = df.loc[0,'Día']

	Cuota.objects.filter(fecha_cuota__year=fecha_cuota.year,
		fecha_cuota__month=fecha_cuota.month).delete()

	for fil, col in df.iterrows():
		connection = engine.raw_connection()
		cursor=connection.cursor()
		cursor.execute("""exec sp_insert_into_cuota
	      @fecha_cuota = '{0}',
	      @cuota_activaciones_total = '{1}',
	      @cuota_altas_total = '{2}',
	      @cuota_activaciones_sp = '{3}',
	      @cuota_activaciones_nosp = '{4}',
	      @cuota_activaciones_prepago = '{5}',
	      @cuota_activaciones_pospago = '{6}',
	      @cuota_activaciones_spmp = '{7}',
	      @cuota_activaciones_spme = '{8}',
	      @cuota_activaciones_nospmp = '{9}',
	      @cuota_activaciones_nospme = '{10}',
	      @cuota_activaciones_spprepago = '{11}',
	      @cuota_activaciones_sppospago = '{12}',
	      @cuota_activaciones_nospprepago = '{13}',
	      @cuota_activaciones_nosppospago = '{14}',
	      @cuota_altas_sp = '{15}',
	      @cuota_altas_nosp = '{16}',
	      @cuota_altas_prepago = '{17}',
	      @cuota_altas_pospago = '{18}',
	      @cuota_altas_spmp = '{19}',
	      @cuota_altas_spme = '{20}',
	      @cuota_altas_nospmp = '{21}',
	      @cuota_altas_nospme = '{22}',
	      @cuota_altas_spprepago = '{23}',
	      @cuota_altas_sppospago = '{24}',
	      @cuota_altas_nospprepago = '{25}',
	      @cuota_altas_nosppospago = '{26}',
	      @cuota_cater_spmp = '{27}',
	      @cuota_cater_spme = '{28}',
	      @cuota_cater_nospmp = '{29}',
	      @cuota_cater_nospme = '{30}',
	      @cuota_tvhd = '{31}',
	      @cuota_tvsd = '{32}',
	      @cuota_fijo = '{33}',
	      @codigo_agente = '{34}'
         """.format(
          col["Día"],
	      col["Cuota Activaciones Total"],
	      col["Cuota Altas Total"],
	      col["Cuota Act. Sp"],
	      col["Cuota Act. No SP"],
	      col["Cuota Act. Prepago"],
	      col["Cuota Act. Pospago"],
	      col["Cuota Act. SP MP"],
	      col["Cuota Act. SP ME"],
	      col["Cuota Act. No SP MP"],
	      col["Cuota Act. No SP ME"],
	      col["Cuota Act. SP Prepago"],
	      col["Cuota Act. SP Pospago"],
	      col["Cuota Act. No SP Prepago"],
	      col["Cuota Act. No SP Pospago"],
	      col["Cuota Altas Sp"],
	      col["Cuota Altas No SP"],
	      col["Cuota Altas Prepago"],
	      col["Cuota Altas Pospago"],
	      col["Cuota Altas SP MP"],
	      col["Cuota Altas SP ME"],
	      col["Cuota Altas No SP MP"],
	      col["Cuota Altas No SP ME"],
	      col["Cuota Altas SP Prepago"],
	      col["Cuota Altas SP Pospago"],
	      col["Cuota Altas No SP Prepago"],
	      col["Cuota Altas No SP Pospago"],
	      col["Cuota Cater SP MP"],
	      col["Cuota Cater SP ME"],
	      col["Cuota Cater No SP MP"],
	      col["Cuota Cater No SP ME"],
	      col["Cuota TV HD"],
	      col["Cuota TV SD"],
	      col["Cuota Fijo"],
	      col["Código de Venta"]
      ))
		cursor.commit()




	return
