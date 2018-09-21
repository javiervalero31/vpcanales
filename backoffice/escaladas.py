from django.shortcuts import render, redirect, HttpResponse
from sqlalchemy import create_engine
import pandas as ps
from xml.etree import ElementTree as et
from django.views.decorators.csrf import csrf_exempt
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
from django.contrib.auth.decorators import login_required


#csrf_exempt es para ignorar el token csrf
@login_required(login_url="/")
@csrf_exempt
def subtabla(request, **kwargs):
    if request.method == 'POST':
        fecha=(request.POST.get('daterange')).split(' hasta ')
        start = datetime.strptime(fecha[0].strip(), "%d-%m-%Y").date()
        end = datetime.strptime(fecha[1].strip(), "%d-%m-%Y").date()
        # se configura precision cero para eliminar las comas
        ps.set_option('precision', 0)
        con = create_engine('postgresql+psycopg2://postgres:alphabeta@10.160.8.96:5432/backoffice')

        table = ps.read_sql_query("""select 'CDS' as canal, count(unaccent("Unidad Operativa")) as total from escaladas where "Unidad Operativa" in (unaccent('CENTRO DE SERVICIO BARINAS'),unaccent('CENTRO DE SERVICIO BARQUISIMETO'), unaccent('CENTRO DE SERVICIO BELLA VISTA'), unaccent('CENTRO DE SERVICIO PARQUE CANAIMA'), unaccent('CENTRO DE SERVICIO CCCT'),unaccent('CENTRO DE SERVICIO GALERIAS MARACAIBO'),unaccent('CENTRO DE SERVICIO LA VIÑA PLAZA'),
         unaccent('CENTRO DE SERVICIO LAS DELICIAS'), unaccent('CENTRO DE SERVICIO LAS GARZAS'), unaccent('CENTRO DE SERVICIO MATURÍN',
         unaccent('CENTRO DE SERVICIO MÉRIDA'), unaccent('CENTRO DE SERVICIO METROCENTER'), unaccent('CENTRO DE SERVICIO PASEO LAS INDUSTRIAS'),
         unaccent('CENTRO DE SERVICIO PORLAMAR'), unaccent('CENTRO DE SERVICIO SAMBIL'), unaccent('CENTRO DE SERVICIO SAN CRISTÓBAL'))and "Fecha Creacion" between '%(start)s 00:00:00' and '%(end)s 23:59:59'
         UNION ALL
         select "Canal Captura" ,COUNT(unaccent("Canal Captura")) as TOTAL FROM escaladas
         WHERE "Canal Captura" in (unaccent('IVR'),unaccent('MMO'),unaccent('REDES SOCIALES'), unaccent('AGENTE AUTORIZADO'), unaccent('ASI')) and "Fecha Creacion" between '%(start)s 00:00:00' and '%(end)s 23:59:59'
         GROUP BY "Canal Captura"
         UNION ALL
         select 'CALL CENTER' AS CANAL, COUNT(unaccent("Canal Captura")) FROM escaladas
         WHERE unaccent("Canal Captura") = unaccent('CALL CENTER') and "Fecha Creacion" between '%(start)s 00:00:00' and '%(end)s 23:59:59'"""%{'start':start, 'end':end}, con)

        treclamos=ps.read_sql_query("""select count("Clasificacion") as Reclamos from escaladas
                                        where unaccent("Clasificacion") = unaccent('RECLAMO') or unaccent("Clasificacion") = unaccent('FALLA O AVERIA') and "Fecha Creacion" between '%s 00:00:00' and '%s 23:59:59'""" %(start, end), con).iloc[0]['reclamos']

        tsolicitud = ps.read_sql_query("""select count(unaccent("Clasificacion")) as SOLICITUD from escaladas
                                            where "Clasificacion" in (unaccent('INSTALACION'),unaccent('OPERACION'), unaccent('SOLICITUD'))
                                        and "Fecha Creacion" between '%s 00:00:00' and '%s 23:59:59'""" %(start, end), con).iloc[0]['solicitud']
        tescaladas= tsolicitud+treclamos

        grafico=table.to_json(orient='records')

        table = et.fromstring(table.to_html(index=False, classes=["table table-bordered table-hover"]))
        table.set('id', 'example1')



        return render(request, 'escaladas.html', {'tabla': et.tostring(table),
                                                    'start': start,
                                                    'end': end,
                                                    'grafico':grafico,
                                                    'treclamos':'{0:,d}'.format(treclamos).replace(',','.'),
                                                    'tsolicitud':'{0:,d}'.format(tsolicitud).replace(',','.'),
                                                    'tescaladas':'{0:,d}'.format(tescaladas).replace(',','.')})

    else:
        def start():
            # se saca la fecha de hoy
            today = date.today()
            # se saca un calculo de del mes anterior
            d = today - relativedelta(months=1)
            # start es el primer dia del mes anterior
            start = date(d.year, d.month, 1).strftime("%d-%m-%Y")
            start = ps.to_datetime(start, format="%d-%m-%Y").strftime("%d-%m-%Y")


            return (start)

        def end():
            today = date.today()
            end = date(today.year, today.month, 1) - relativedelta(days=1)
            end = end.strftime("%d-%m-%Y")
            end = ps.to_datetime(end, format="%d-%m-%Y").strftime("%d-%m-%Y")

            return (end)

            # Se reciben los argumentos start y end

        start = kwargs.get('start', start())
        end = kwargs.get('end', end())
        start = datetime.strptime(start, "%d-%m-%Y").date()
        end = datetime.strptime(end, "%d-%m-%Y").date()

        # se configura precision cero para eliminar las comas
        ps.set_option('precision', 0)
        con = create_engine('postgresql+psycopg2://postgres:alphabeta@localhost:5432/backoffice')

        table = ps.read_sql_query("""select unaccent('CDS') as canal, count(unaccent("Unidad Operativa")) as total from escaladas where unaccent("Unidad Operativa") in (unaccent('CENTRO DE SERVICIO BARINAS'),unaccent('CENTRO DE SERVICIO BARQUISIMETO'), unaccent('CENTRO DE SERVICIO BELLA VISTA'), unaccent('CENTRO DE SERVICIO PARQUE CANAIMA'), unaccent('CENTRO DE SERVICIO CCCT'), unaccent('CENTRO DE SERVICIO GALERIAS MARACAIBO'), unaccent('CENTRO DE SERVICIO LA VIÑA PLAZA'),
         unaccent('CENTRO DE SERVICIO LAS DELICIAS'), unaccent('CENTRO DE SERVICIO LAS GARZAS'), unaccent('CENTRO DE SERVICIO MATURÍN'),
         unaccent('CENTRO DE SERVICIO MÉRIDA'), unaccent('CENTRO DE SERVICIO METROCENTER'), unaccent('CENTRO DE SERVICIO PASEO LAS INDUSTRIAS'),
         unaccent('CENTRO DE SERVICIO PORLAMAR'), unaccent('CENTRO DE SERVICIO SAMBIL'), unaccent('CENTRO DE SERVICIO SAN CRISTÓBAL'))and "Fecha Creacion" between '%(start)s 00:00:00' and '%(end)s 23:59:59'
         UNION ALL
         select unaccent("Canal Captura") ,COUNT(unaccent("Canal Captura")) as TOTAL FROM escaladas
         WHERE "Canal Captura" in (unaccent('IVR'), unaccent('MMO'), unaccent('REDES SOCIALES'), unaccent('AGENTE AUTORIZADO'), unaccent('ASI')) and "Fecha Creacion" between '%(start)s 00:00:00' and '%(end)s 23:59:59'
         GROUP BY unaccent("Canal Captura")
         UNION ALL
         select unaccent('CALL CENTER') AS CANAL, COUNT(unaccent("Canal Captura")) FROM escaladas
         WHERE unaccent("Canal Captura") = unaccent('CALL CENTER') and "Fecha Creacion" between '%(start)s 00:00:00' and '%(end)s 23:59:59'"""%{'start':start, 'end':end}, con)

        treclamos=ps.read_sql_query("""select count(unaccent("Clasificacion")) as Reclamos from escaladas
                                        where unaccent("Clasificacion") in (unaccent('RECLAMO'), unaccent('FALLA O AVERIA')) and "Fecha Creacion" between '%s 00:00:00' and '%s 23:59:59'""" %(start, end), con).iloc[0]['reclamos']

        tsolicitud = ps.read_sql_query("""select count(unaccent("Clasificacion")) as SOLICITUD from escaladas
                                        where unaccent("Clasificacion") in (unaccent('INSTALACION'), unaccent('OPERACION'), unaccent('SOLICITUD'))
                                        and "Fecha Creacion" between '%s 00:00:00' and '%s 23:59:59'""" %(start, end), con).iloc[0]['solicitud']
        tescaladas= tsolicitud+treclamos

        grafico=table.to_json(orient='records')

        table = et.fromstring(table.to_html(index=False, classes=["table table-bordered table-hover"]))
        table.set('id', 'example1')



        return render(request, 'escaladas.html', {'tabla': et.tostring(table),
                                                    'start': start,
                                                    'end': end,
                                                    'grafico':grafico,
                                                    'treclamos':'{0:,d}'.format(treclamos).replace(',','.'),
                                                    'tsolicitud':'{0:,d}'.format(tsolicitud).replace(',','.'),
                                                    'tescaladas':'{0:,d}'.format(tescaladas).replace(',','.')})
