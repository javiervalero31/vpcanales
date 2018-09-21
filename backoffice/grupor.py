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


        ps.set_option('precision', 0)

        con = create_engine('postgresql://postgres:alphabeta@localhost:5432/backoffice')
        table = ps.read_sql_query("""
select t1."Grupo Resolutor", t1."Bandeja Resolutor", t1.escaladas, t2.resueltas, t3.me,  CONCAT(ROUND((cast(t2.Resueltas AS DECIMAL)/t1.Escaladas)*100,2), '%(porcentaje)s') AS RATIO
FROM
(select "Grupo Resolutor","Bandeja Resolutor", count ("Bandeja Resolutor") as escaladas from escaladas where "Fecha Creacion" between '%(start)s' and '%(end)s'
group by "Bandeja Resolutor", "Grupo Resolutor"
order by "Grupo Resolutor")as t1,

(select "Grupo Resolutor","Bandeja Resolutor", count ("Bandeja Resolutor")as resueltas from resueltas where "Fecha/Hora Solucion" between '%(start)s' and '%(end)s'
group by "Bandeja Resolutor", "Grupo Resolutor"
order by "Grupo Resolutor")as t2,

(select "Grupo Resolutor","Bandeja Resolutor", SUM (CASE "Sub Estado" WHEN 'MAL ESCALADO' THEN 1 ELSE 0 END) as me from resueltas where "Fecha/Hora Solucion" between '%(start)s' and '%(end)s'
group by "Bandeja Resolutor", "Grupo Resolutor"
order by "Grupo Resolutor")as t3


where t1."Bandeja Resolutor" = t2."Bandeja Resolutor" and t1."Bandeja Resolutor" = t3."Bandeja Resolutor"

            """%{'start':start, 'end':end, 'porcentaje':'%%'}, con)

        grafico = table.to_html()

        table = et.fromstring(table.to_html(index=False, classes=["table table-bordered table-hover"]))
        # parametros adicionales para la tabla
        table.set('id', 'example1')
        return render(request, 'gruporesolutor.html', {'tabla': et.tostring(table),
                                                   'start': start,
                                                   'end': end,
                                                   'grafico': grafico})

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
        start = kwargs.get('start',start())
        end = kwargs.get('end', end())
        start = datetime.strptime(start, "%d-%m-%Y").date()
        end = datetime.strptime(end, "%d-%m-%Y").date()

        ps.set_option('precision', 0)

        con = create_engine('postgresql://postgres:alphabeta@localhost:5432/backoffice')
        table = ps.read_sql_query("""
        select t1."Grupo Resolutor", t1."Bandeja Resolutor", t1.escaladas, t2.resueltas, t3.me,  CONCAT(ROUND((cast(t2.Resueltas AS DECIMAL)/t1.Escaladas)*100,2), '%(porcentaje)s') AS RATIO
        FROM
        (select "Grupo Resolutor","Bandeja Resolutor", count ("Bandeja Resolutor") as escaladas from escaladas where "Fecha Creacion" between '%(start)s' and '%(end)s'
        group by "Bandeja Resolutor", "Grupo Resolutor"
        order by "Grupo Resolutor")as t1,

        (select "Grupo Resolutor","Bandeja Resolutor", count ("Bandeja Resolutor")as resueltas from resueltas where "Fecha/Hora Solucion" between '%(start)s' and '%(end)s'
        group by "Bandeja Resolutor", "Grupo Resolutor"
        order by "Grupo Resolutor")as t2,

        (select "Grupo Resolutor","Bandeja Resolutor", SUM (CASE "Sub Estado" WHEN 'MAL ESCALADO' THEN 1 ELSE 0 END) as me from resueltas where "Fecha/Hora Solucion" between '%(start)s' and '%(end)s'
        group by "Bandeja Resolutor", "Grupo Resolutor"
        order by "Grupo Resolutor")as t3


        where t1."Bandeja Resolutor" = t2."Bandeja Resolutor" and t1."Bandeja Resolutor" = t3."Bandeja Resolutor"

                    """%{'start':start, 'end':end, 'porcentaje':'%%'}, con)


    #Aqui se realiza el JSON que consume el grafico
        grafico = table.set_index('Grupo Resolutor').to_json(orient='records')
        # se convierte en tabla html
        table = et.fromstring(table.to_html(index=False, classes=["table table-bordered table-hover"]))
        # parametros adicionales para la tabla
        table.set('id', 'example1')
        return render(request, 'gruporesolutor.html', {'tabla': et.tostring(table),
                                                   'start': start,
                                                   'end': end,
                                                   'grafico': grafico})
