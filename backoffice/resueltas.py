from django.shortcuts import render, redirect, HttpResponse
from sqlalchemy import create_engine
import pandas as ps
from xml.etree import ElementTree as et
from django.views.decorators.csrf import csrf_exempt
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
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

        con = create_engine('postgresql+psycopg2://postgres:alphabeta@10.160.8.96:5432/backoffice')
        table = ps.read_sql_query("""select   unaccent("Grupo Resolutor"), unaccent("Sub Estado"),  count(unaccent("Sub Estado")) AS Total from resueltas
                                    WHERE "Fecha/Hora Solucion" between '%s 00:00:00' and '%s 23:59:59'
                                    GROUP BY "Sub Estado", "Grupo Resolutor"
                                    ORDER BY "Grupo Resolutor"; """%(start, end), con)
        tabledetail = ps.read_sql_query("""
            select t1."Grupo Resolutor", t1."Bandeja Resolutor", t1.escaladas, t2.resueltas, t3.me,  CONCAT(ROUND((cast(t2.Resueltas AS DECIMAL)/t1.Escaladas)*100,2), '%(porcentaje)s') AS RATIO
            FROM
            (select "Grupo Resolutor","Bandeja Resolutor", count ("Bandeja Resolutor") as escaladas from escaladas where "Fecha Creacion" between '%(start)s 00:00:00' and '%(end)s 23:59:59'
            group by "Bandeja Resolutor", "Grupo Resolutor"
            order by "Grupo Resolutor")as t1,

            (select "Grupo Resolutor","Bandeja Resolutor", count ("Bandeja Resolutor")as resueltas from resueltas where "Fecha/Hora Solucion" between '%(start)s 00:00:00' and '%(end)s 23:59:59'
            group by "Bandeja Resolutor", "Grupo Resolutor"
            order by "Grupo Resolutor")as t2,

            (select "Grupo Resolutor","Bandeja Resolutor", SUM (CASE unaccent("Sub Estado") WHEN unaccent('MAL ESCALADO') THEN 1 ELSE 0 END) as me from resueltas where "Fecha/Hora Solucion" between '%(start)s 00:00:00' and '%(end)s 23:59:59'
            group by "Bandeja Resolutor", "Grupo Resolutor"
            order by "Grupo Resolutor")as t3


            where t1."Bandeja Resolutor" = t2."Bandeja Resolutor" and t1."Bandeja Resolutor" = t3."Bandeja Resolutor"

            """%{'start':start, 'end':end, 'porcentaje':'%%'}, con)
        tabledetail=tabledetail.rename(columns={'escaladas':'Escaladas','resueltas':'Resueltas','me':'Mal Escaladas','ratio':'Ratio'})

    #Aqui se realiza el JSON que consume el grafico
        table2= ps.read_sql_query("""select   unaccent("Grupo Resolutor") as "Grupo Resolutor" , unaccent("Sub Estado") as "Sub Estado"  from resueltas
                                    WHERE "Fecha/Hora Solucion" between '%s 00:00:00' and '%s 23:59:59'"""%(start, end), con)

        table2= table2.groupby(['Grupo Resolutor', 'Sub Estado']).size()
        a = table2.index.levels[0]

        df = table2.append(ps.Series(a, index=[a, ['Grupo Resolutor'] * len(a)]))

        d = [v.reset_index(level=0, drop=True).to_dict() for k,v in df.groupby(level=0)]

        import json

        with open('result.json', 'w') as fp:
            json.dump(d, fp)

        j = df.unstack().to_json(orient='records')


        grafico = j
    #Fin de Grafico

        treclamos = ps.read_sql_query("""select count(unaccent("Clasificacion")) as Reclamos from resueltas
                                        where unaccent("Clasificacion") in (unaccent('RECLAMO'), unaccent('FALLA O AVERIA')) and "Fecha/Hora Solucion" between '%s 00:00:00' and '%s 23:59:59'""" %(start, end), con).iloc[0]['reclamos']

        tsolicitud = ps.read_sql_query("""select count("Clasificacion") as SOLICITUD from resueltas
                                        where unaccent("Clasificacion") in (unaccent('INSTALACION'), unaccent('OPERACION'), unaccent('SOLICITUD'),unaccent('OPERACIÓN'))
                                        and "Fecha/Hora Solucion" between '%s 00:00:00' and '%s 23:59:59'""" %(start, end), con).iloc[0]['solicitud']

        tresueltas= tsolicitud+treclamos



        tme = ps.read_sql_query("""select count("Sub Estado")
                                    from resueltas
                                    where unaccent("Sub Estado") =unaccent('MAL ESCALADO')
                                    and "Fecha/Hora Solucion" between '%s 00:00:00' and '%s 23:59:59'""" %(start, end), con).iloc[0]['count']


        # se convierte en tabla html
        table = et.fromstring(table.to_html(index=False, classes=["table table-bordered table-hover"]))
        tabledetail = et.fromstring(tabledetail.to_html(index=False, classes=["table table-bordered table-hover"]))
        # parametros adicionales para la tabla
        mini = ps.read_sql_query("""select min("Fecha/Hora Solucion")from resueltas""",con).iloc[0]
        maxi = ps.read_sql_query("""select max("Fecha/Hora Solucion")from resueltas""",con).iloc[0]
        tabledetail.set('id','example2')
        table.set('id', 'example1')
        print(table)
        return render(request, 'subestados.html', {'tabla': et.tostring(table),
                                                   'start': start,
                                                   'end': end,
                                                   'treclamos': treclamos,
                                                   'tsolicitud': tsolicitud,
                                                   'tresueltas': tresueltas,
                                                   'tme': tme,
                                                   'grafico': grafico,
                                                   'maxi':maxi,
                                                   'mini':mini,
                                                   'tabledetail':et.tostring(tabledetail)})
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
        start = start()
        end = end()
        start = datetime.strptime(start, "%d-%m-%Y").date()
        end = datetime.strptime(end, "%d-%m-%Y").date()

        ps.set_option('precision', 0)


        con = create_engine('postgresql://postgres:alphabeta@localhost:5432/backoffice')
        table = ps.read_sql_query("""select   "Grupo Resolutor", "Sub Estado",  count("Sub Estado") AS Total from resueltas
                                    WHERE "Fecha/Hora Solucion" BETWEEN '%s' AND '%s'
                                    GROUP BY "Sub Estado", "Grupo Resolutor"
                                    ORDER BY "Grupo Resolutor"; """%(start, end), con)

        tabledetail = ps.read_sql_query("""
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

        tabledetail=tabledetail.rename(columns={'escaladas':'Escaladas','resueltas':'Resueltas','me':'Mal Escaladas','ratio':'Ratio'})


    #Aqui se realiza el JSON que consume el grafico
        table2= ps.read_sql_query("""select   "Grupo Resolutor", "Sub Estado" from resueltas
                                    WHERE "Fecha/Hora Solucion" BETWEEN '%s' AND '%s'"""%(start, end), con)

        table2= table2.groupby(['Grupo Resolutor', 'Sub Estado']).size()
        a = table2.index.levels[0]

        df = table2.append(ps.Series(a, index=[a, ['Grupo Resolutor'] * len(a)]))

        d = [v.reset_index(level=0, drop=True).to_dict() for k,v in df.groupby(level=0)]

        import json

        with open('result.json', 'w') as fp:
            json.dump(d, fp)

        j = df.unstack().to_json(orient='records')


        grafico = j
    #Fin de Grafico

        treclamos = ps.read_sql_query("""select count("Clasificacion") as Reclamos from resueltas
                                        where "Clasificacion" in (unaccent('RECLAMO'), unaccent('FALLA O AVERIA')) and "Fecha/Hora Solucion" between '%s' and '%s'""" %(start, end), con).iloc[0]['reclamos']

        tsolicitud = ps.read_sql_query("""select count("Clasificacion") as SOLICITUD from resueltas
                                        where "Clasificacion" in (unaccent('INSTALACION'), unaccent('OPERACION'), unaccent('SOLICITUD'))
                                        and "Fecha/Hora Solucion" between '%s' and '%s'""" %(start, end), con).iloc[0]['solicitud']

        tresueltas= tsolicitud+treclamos

        tme = ps.read_sql_query("""select count("Sub Estado")
                                    from resueltas
                                    where unaccent("Sub Estado") =unaccent('MAL ESCALADO')
                                    and "Fecha/Hora Solucion" between '%s' and '%s'""" %(start, end), con).iloc[0]['count']

        mini = ps.read_sql_query("""select min("Fecha/Hora Solucion")from resueltas""",con).iloc[0]
        maxi = ps.read_sql_query("""select max("Fecha/Hora Solucion")from resueltas""",con).iloc[0]
        tabledetail = et.fromstring(tabledetail.to_html(index=False, classes=["table table-bordered table-hover"]))
        tabledetail.set('id','example2')

        # se convierte en tabla html
        table = et.fromstring(table.to_html(index=False, classes=["table table-bordered table-hover"]))
        # parametros adicionales para la tabla
        table.set('id', 'example1')
        return render(request, 'subestados.html', {'tabla': et.tostring(table),
                                                   'start': start,
                                                   'end': end,
                                                   'treclamos': treclamos,
                                                   'tsolicitud': tsolicitud,
                                                   'tresueltas': tresueltas,
                                                   'tme': tme,
                                                   'grafico': grafico,
                                                   'maxi':maxi,
                                                   'mini':mini,
                                                   'tabledetail':et.tostring(tabledetail)})
