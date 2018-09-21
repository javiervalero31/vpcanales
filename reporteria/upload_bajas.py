from django.shortcuts import render
from .models import *
import pyodbc
import time
from datetime import datetime, date
import pandas as pd
from sqlalchemy import create_engine
import logging as log
from pandas import to_datetime

from django.db.models import  Sum



def index_update_bajas(engine):
    connection = engine.raw_connection()
    cursor=connection.cursor()
    cursor.execute("""IF NOT EXISTS (SELECT
                        *
                      FROM index_actividad
                      WHERE ano = (SELECT
                        YEAR(MAX(fecha_actividad))
                      FROM reporteria_baja)
                      AND mes = (SELECT
                        MONTH(MAX(fecha_actividad))
                      FROM reporteria_baja))

                    BEGIN

                      INSERT INTO index_actividad

                        SELECT
                          LEFT(DATENAME(MONTH, t4.fechamax), 20) + ' ' + RIGHT('00' + CAST(YEAR(t4.fechamax) AS varchar), 4) AS Year,
                          t1.Actividad AS activaciones,
                          t2.Altas AS altas,
                          t3.Bajas AS bajas,
                          t4.ano,
                          t4.mes
                        FROM (SELECT
                               SUM(cantidad) AS Actividad
                             FROM reporteria_activacion
                             WHERE YEAR(fecha_actividad) = (SELECT
                               YEAR(MAX(fecha_actividad))
                             FROM reporteria_baja)
                             AND MONTH(fecha_actividad) = (SELECT
                               MONTH(MAX(fecha_actividad))
                             FROM reporteria_baja)) t1,

                             (SELECT
                               SUM(cantidad) AS Altas
                             FROM reporteria_alta
                             WHERE YEAR(fecha_actividad) = (SELECT
                               YEAR(MAX(fecha_actividad))
                             FROM reporteria_baja)
                             AND MONTH(fecha_actividad) = (SELECT
                               MONTH(MAX(fecha_actividad))
                             FROM reporteria_baja)) t2,
                             (SELECT
                               SUM(neta) AS Bajas
                             FROM reporteria_baja
                             WHERE YEAR(fecha_actividad) = (SELECT
                               YEAR(MAX(fecha_actividad))
                             FROM reporteria_baja)
                             AND MONTH(fecha_actividad) = (SELECT
                               MONTH(MAX(fecha_actividad))
                             FROM reporteria_baja)) t3,
                             (SELECT
                               MAX(fecha_actividad) AS fechamax,
                               MONTH(MAX(fecha_actividad)) AS mes,
                               YEAR(MAX(fecha_actividad)) AS ano
                             FROM reporteria_Baja) t4

                    END

                    ELSE

                    BEGIN
                      WITH refresh
                      AS (SELECT
                        LEFT(DATENAME(MONTH, t4.fechamax), 20) + ' ' + RIGHT('00' + CAST(YEAR(t4.fechamax) AS varchar), 4) AS Year,
                        t1.Actividad AS activaciones,
                        t2.Altas AS altas,
                        t3.Bajas AS bajas,
                        t4.ano,
                        t4.mes
                      FROM (SELECT
                             SUM(cantidad) AS Actividad
                           FROM reporteria_activacion
                           WHERE YEAR(fecha_actividad) = (SELECT
                             YEAR(MAX(fecha_actividad))
                           FROM reporteria_baja)
                           AND MONTH(fecha_actividad) = (SELECT
                             MONTH(MAX(fecha_actividad))
                           FROM reporteria_baja)) t1,

                           (SELECT
                             SUM(cantidad) AS Altas
                           FROM reporteria_alta
                           WHERE YEAR(fecha_actividad) = (SELECT
                             YEAR(MAX(fecha_actividad))
                           FROM reporteria_baja)
                           AND MONTH(fecha_actividad) = (SELECT
                             MONTH(MAX(fecha_actividad))
                           FROM reporteria_baja)) t2,
                           (SELECT
                             SUM(neta) AS Bajas
                           FROM reporteria_baja
                           WHERE YEAR(fecha_actividad) = (SELECT
                             YEAR(MAX(fecha_actividad))
                           FROM reporteria_baja)
                           AND MONTH(fecha_actividad) = (SELECT
                             MONTH(MAX(fecha_actividad))
                           FROM reporteria_baja)) t3,
                           (SELECT
                             MAX(fecha_actividad) AS fechamax,
                             MONTH(MAX(fecha_actividad)) AS mes,
                             YEAR(MAX(fecha_actividad)) AS ano
                           FROM reporteria_Baja) t4)
                      UPDATE index_actividad
                      SET year = refresh.year,
                          index_actividad.activaciones = refresh.activaciones,
                          index_actividad.altas = refresh.altas,
                          index_actividad.bajas = refresh.bajas,
                          index_actividad.ano = refresh.ano,
                          index_actividad.mes = refresh.mes
                      FROM refresh
                    END""")
    cursor.commit()
    return



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
def uploader_bajas(df):
	engine = create_engine("mssql+pyodbc://sa:BaseSQL123@10.160.8.96:1433/VPCANALES?driver=SQL+Server+Native+Client+11.0")

	fecha = df.loc[0,'Periodo']

	Baja.objects.filter(fecha_actividad__year=fecha.year,
		fecha_actividad__month=fecha.month).delete()

	for row in df.itertuples():
	    connection = engine.raw_connection()
	    cursor=connection.cursor()
	    cursor.execute("""exec sp_insert_into_baja
	    @fecha_actividad='{0}',
	    @plataforma='{1}',
	    @tecnologia='{2}',
	    @terminal='{3}',
	    @bruta='{4}',
	    @reactivada='{5}',
	    @neta = '{6}',
	    @codigo_plan='{7}',
	    @mes={8},
	    @ano={9},
	    @codigo_agente='{10}'
	     """.format(row[1],
	    row[5],
	    row[6],
	    row[7],
	    row[8],
	    row[9],
	    row[-2],
	    row[4],
	    row[1].month,
	    row[1].year,
	    row[3]))
	    cursor.commit()



	index_update_bajas(engine)
	return
