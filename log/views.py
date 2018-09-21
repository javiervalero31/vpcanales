#!python
# log/resueltas.py
from django.shortcuts import render, redirect, HttpResponse
from sqlalchemy import create_engine
import pandas as pd
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from recargas.models import *
from reporteria.models import *
from datetime import timedelta
from django.db.models import Sum, Max

@login_required(login_url="login/")
def home(request):
    engine = create_engine("mssql+pyodbc://sa:BaseSQL123@10.160.8.96:1433/vpcanales?driver=SQL+Server+Native+Client+11.0")
    today = date.today()

    # Resumen de Actividad
    resumenActividad = """select * from index_actividad"""

    ra = pd.read_sql_query(resumenActividad, engine)
    ra.altas = ra.altas.astype(int)
    ra.activaciones = ra.activaciones.astype(int)

    ultimate_date = Activacion.objects.values_list('fecha_actividad',flat=True)\
    .latest('fecha_actividad')

    act = Activacion.objects.filter(fecha_actividad__year=ultimate_date.year,
                                fecha_actividad__month=ultimate_date.month,
                                ).values('cantidad','fecha_actividad').aggregate(Sum('cantidad'), Max('fecha_actividad'))

    # ca2=ca.get('fecha_actividad__max')

    alt = Alta.objects.filter(fecha_actividad__year=ultimate_date.year,
                            fecha_actividad__month=ultimate_date.month,
                            ).values('cantidad','fecha_actividad').aggregate(Sum('cantidad'), Max('fecha_actividad'))

    conv = alt.get('cantidad__sum') / act.get('cantidad__sum') * 100


    ultimate_date_venta = Venta.objects.values('tiempo__fecha').exclude(monto__exact=0)\
                                       .order_by('-tiempo__fecha')[0]['tiempo__fecha']

    re=Venta.objects.filter(tiempo__fecha__year=ultimate_date_venta.year,
                            tiempo__fecha__month=ultimate_date_venta.month)\
                            .aggregate(Sum('monto'))

    # Cantidad de activaciones del mes pasado:
    resumenBackoffice="""select * from index_gestionr"""

    rb=pd.read_sql_query(resumenBackoffice, engine)
    rb.escaladas.astype(int)
    rb.resueltas.astype(int)

    es=rb.loc[rb.tail(1).index.item(),'escaladas']

    aaasi = '''select * from index_arcgis'''
    puntos=pd.read_sql_query(aaasi, engine)

    #MES ABIERTO
    resumenActividad_diaria="""
     SELECT ACTIVACIONES_ABIERTAS.fecha, ACTIVACIONES_ABIERTAS.activaciones , ALTAS_ABIERTAS.altas  FROM
         (SELECT sum(a.CANTIDAD) ACTIVACIONES , CONCAT(DATENAME(month, a.fecha_actividad),' ', DATENAME(YEAR, a.fecha_actividad)) Fecha
          FROM reporteria_activacion a
          WHERE MONTH(FECHA_ACTIVIDAD) IN (
             SELECT month(max(FECHA_ACTIVIDAD)) FROM reporteria_activacion)
          AND YEAR(FECHA_ACTIVIDAD) IN (
             SELECT year(max(FECHA_ACTIVIDAD)) FROM reporteria_activacion)
          GROUP BY CONCAT(DATENAME(month, a.fecha_actividad),' ', DATENAME(YEAR, a.fecha_actividad))
      ) ACTIVACIONES_ABIERTAS,

         (SELECT sum(a.CANTIDAD) ALTAS
          FROM reporteria_alta a
          WHERE MONTH(FECHA_ACTIVIDAD) IN (
             SELECT month(max(FECHA_ACTIVIDAD)) FROM reporteria_alta)
          AND YEAR(FECHA_ACTIVIDAD) IN (
             SELECT year(max(FECHA_ACTIVIDAD)) FROM reporteria_alta)
      ) ALTAS_ABIERTAS
    """

    ma = pd.read_sql_query(resumenActividad_diaria, engine)
    ma.activaciones = ma.activaciones.astype(int)
    ma.altas = ma.altas.astype(int)
    fecha = ma.tail(1).iloc[0,0]
    ma_act = ma.tail(1).iloc[0,1]
    ma_alt = ma.tail(1).iloc[0,2]

    return render(request, "home.html",{'ra':ra,
                                        # 'ca2':ca2,
                                        'act':act.get('cantidad__sum'),
                                        'act_fecha':act.get('fecha_actividad__max'),
                                        'alt_fecha':alt.get('fecha_actividad__max'),
                                        'alt':alt.get('cantidad__sum'),
                                        'es':'{0:,d}'.format(es).replace(',','.'),
                                        're':re.get('monto__sum'),
                                        're_fecha':  ultimate_date_venta,
                                        'conv' : conv,
                                        'rb':rb,
                                        'puntos':puntos,
                                        'ma':ma})

def mail_informativo(request):
    from django.core.mail import send_mail
    from django.template import loader

    max_date = Activacion.objects.values_list('fecha_carga',flat=True).latest('fecha_carga')
    reporteria = max_date - timedelta(days=2)
    recarga = Venta.objects.values('tiempo__fecha').exclude(monto__exact=0)\
                           .order_by('-tiempo__fecha')[0]['tiempo__fecha']

    html_message = loader.render_to_string(
                    "mail_informativo.html", {'recarga':recarga,'reporteria':reporteria}
                    )
    send_mail('Actualizacion Diaria de Vp.Canales', '', 'GciaAnaliticaComercial.ve@telefonica.com',list(User.objects.filter(is_active=1).values_list('email', flat=True)), fail_silently=False,html_message=html_message)
    return render(request, "messages.html",{'message':'Correo Enviado con exito'} )

    # codigo = 'VI2131245'
    # html_message = loader.render_to_string("jerarquia_aprobacion_mail.html",{'codigo':codigo})
    # send_mail('Actualizacion Diaria de Vp.Canales', '', 'GciaAnaliticaComercial.ve@telefonica.com',['anthony.nardelli@telefonica.com'], fail_silently=False,html_message=html_message)
    # return render(request, "jerarquia_aprobacion_mail.html",{'codigo':codigo} )

def index_update(request):
    engine = create_engine("mssql+pyodbc://sa:BaseSQL123@10.160.8.96:1433/VPCANALES?driver=SQL+Server+Native+Client+11.0")
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
    return render(request, "messages.html",{'message':'Actualizado con exito'})
