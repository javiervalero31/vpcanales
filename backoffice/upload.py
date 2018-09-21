from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
import pandas as ps
from sqlalchemy import create_engine
from django.contrib import messages
import os
from pandas.io import sql

liste = ['Categoria*', 'Tipo*', 'Elemento*', 'Razon*', 'Estado',
         'Sub Estado',
         'Ciclo Fact', 'Tipo Cuenta', 'Status del Servicio', 'Plataforma', 'Tecnologia', 'Segmentacion',
         'Fecha Creacion','Clasificacion',
         'Creado Por', 'Bandeja Resolutor', 'Grupo Resolutor', 'Unidad Operativa',
         'Canal Captura', 'Reabierto?', 'Reasignado?', 'Retipificado?',
         'Region', 'Monto Ajuste', 'Plan', 'Marca Equipo', 'Cliente_Reincidente',
         'Linea de Negocio',
         'id_subida']
listr = ['Categoria*', 'Tipo*', 'Elemento*', 'Razon*', 'Estado',
         'Sub Estado','Clasificacion',
         'Ciclo Fact', 'Tipo Cuenta', 'Status del Servicio', 'Plataforma', 'Tecnologia', 'Segmentacion',
         'Fecha/Hora Solucion', 'Creado Por', 'Bandeja Resolutor', 'Grupo Resolutor', 'Unidad Operativa',
         'Canal Captura', 'Reabierto?', 'Reasignado?', 'Retipificado?',
         'Region', 'Monto Ajuste', 'Plan', 'Marca Equipo', 'En Horas_TV', 'En Horas', 'Cliente_Reincidente',
         'Linea de Negocio',
         'id_subida']

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            ruta_insumo = request.FILES.get('file')
            tipo = request.POST.get('tipo')
            date = request.POST.get('date_month')+request.POST.get('date_year')
            print(date)

            if tipo == 'E':
                #lee el archivo en la direccion local
                reader = ps.read_excel(ruta_insumo, sheet_name='ESCALADAS')
                # guardo la variable de fecha en T
                t = date
                #Creo una columna y le asigno una id
                reader['id_subida']= 'e'+t
                #Selecciono solo las columnas que me interesan
                reader = reader[liste]
                #Este es el motor que usamos para comunicarnos con la base de datos
                engine = create_engine('postgresql://postgres:alphabeta@localhost:5432/backoffice')
                ce = "'e"
                c= "'"
                #Elimina lo que tenga id subida que coincida con el mes
                sql.execute('DELETE FROM escaladas WHERE "id_subida" =%s' % ce + t + c, engine)
                #Paso el archivo a la base de datos y si exite se agrega con una nueva ID
                reader.to_sql(name="escaladas", con=engine, if_exists="append", index=False)
                #Cuando termine la linea anterior se actualiza el estado del archivo a T que es importado

                #Este print es solo para saber que el proceso fue ejecutado correctamente (solo se vera en consola)
                print("OK")
            else:
                # lee el archivo en la direccion local
                reader = ps.read_excel(ruta_insumo, sheet_name='RESUELTAS')
                # guardo la variable de fecha en T
                t = date
                # Creo una columna y le asigno una id
                reader['id_subida'] = 'r' + t
                # Selecciono solo las columnas que me interesan
                reader = reader[listr]
                # Este es el motor que usamos para comunicarnos con la base de datos
                engine = create_engine('postgresql://postgres:alphabeta@localhost:5432/backoffice')
                ce = "'r"
                c = "'"
                # Elimina lo que tenga id subida que coincida con el mes
                sql.execute('DELETE FROM resueltas WHERE "id_subida" =%s' % ce + t + c, engine)
                # Paso el archivo a la base de datos y si exite se agrega con una nueva ID
                reader.to_sql(name="resueltas", con=engine, if_exists="append", index=False)
                # Cuando termine la linea anterior se actualiza el estado del archivo a T que es importado

                # Este print es solo para saber que el proceso fue ejecutado correctamente (solo se vera en consola)
                print("OK")

    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
