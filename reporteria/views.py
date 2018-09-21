from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from openpyxl import load_workbook
from .forms import JerarquiaPlanes, Actividades
from .models import *

import os
import pandas as pd
from datetime import *
from time import time
import pyodbc
from xml.etree import ElementTree as et
from .query_builder import *
from xlsxwriter.workbook import Workbook
import io
from django.contrib.auth.decorators import login_required
from urllib.request import urlopen
import ssl


context = ssl._create_unverified_context()
@login_required(login_url="/")
def reporte(request):


    if request.method == 'POST':

        datos=[] #Datos por defecto en reporte

        fechas=[ ]

        date=(request.POST.get('daterange')).split(' to ')

        fechas.append(date[0].strip()) #verificar si hay espacio al final o al inicio del str
        fechas.append(date[1].strip())

        for id,value in request.POST.items():
            if id =='csrfmiddlewaretoken' or id=='daterange':
                continue
            elif id == 'actividad':
                actividad=value

            else:
                datos.append(id)


        a=actividad.title()
        print("Los Datos solicitados son: ",datos)


        data=query_builder(fechas,actividad,datos)

        preview = et.fromstring(data.head(100).to_html(index=False, classes=["table table-bordered table-hover"]))
        preview.set('id', 'example1')

        out= io.BytesIO()
        writer = pd.ExcelWriter(out,engine='xlsxwriter')
        writer.book.filename = out

        data.to_excel(writer,sheet_name=a, index=False, startrow=4)
        workbook = writer.book
        worksheet = writer.sheets[a]
        image_width =500.0
        image_height = 450.0
        cell_width = 64.0
        cell_height = 15.0
        x_scale = cell_width/image_width
        y_scale = cell_width/image_height
        ruta= 'static\excel\logo.png'
        worksheet.insert_image('A1', ruta,{'x_scale':x_scale, 'y_scale':y_scale })

        header_format = workbook.add_format({
        'bold':True,
        'text_wrap':True,
        'valign':'top',
        'fg_color':'#2593B5',
        'border':0,
        'font_color': 'white',
        'align':'center'
        })
        worksheet.write("D1","Vicepresidencia de Canales")
        worksheet.write("D2","Direccion de Planificacion de Canales")
        worksheet.write("D3","Gerencia de Analitica de Canales")
        worksheet.write("G2","Desde:")
        worksheet.write("G3","Hasta:")
        worksheet.write("H2",fechas[0])
        worksheet.write("H3",fechas[1])
        for col_num, value in enumerate(data.columns.values):
            worksheet.write(4, col_num, value, header_format)
        worksheet.set_column('A:Z',13)
        writer.save()
        out.seek(0)
        response = HttpResponse(out.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = "attachment; filename='Reporte.xlsx'"

		# return render(request, 'reporteria.html', {'tabla': et.tostring(preview)})
        return response
    else:
        max_date=Activacion.objects.values_list('fecha_carga',flat=True).latest('fecha_carga')
        max_date = max_date - timedelta(days=2)

        contexto = {'fecha_completa':max_date,
        'fecha':str(max_date)}

        return render (request,"reporteria.html",contexto)


def comercial_grafica(request):
    return render(request,"displayer.html")

    
def abrirModal(request):
    return render(request,"prueba2.html")
