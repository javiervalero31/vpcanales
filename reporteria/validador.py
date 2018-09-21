import pandas as pd
from django.contrib import messages
from .forms import *
from django.shortcuts import render
from .upload_jp import uploader_jp
from .upload_actividad import uploader_actividad #Activaciones o Altas
from .upload_bajas import uploader_bajas
from .upload_cuotas import uploader_cuotas
from datetime import *
from time import time
from .models import *

def go(request, validado, msj, **kwargs):
    """ Ejecuta los uploaders en funcion a VALIDADO """



    if validado==False:
        mensaje=msj + """
                        <div class = "col-md-2 col-lg-2 col-xs-2">
                           <button type="button" class="btn btn-block btn-primary" onclick="goBack()" >
                           Volver a intentar
                           </button>
                        </div>


                        <script>
                           function goBack() {
                               window.history.back();}
                        </script>"""
        return render(request, "messages.html", {'message': mensaje})


    #uploader activaciones_altas
    elif (validado==True and "df_act" in kwargs.keys() and "df_alt" in kwargs.keys() ):

        results_activaciones = uploader_actividad(kwargs.get("df_act"), Activacion)
        results_altas = uploader_actividad(kwargs.get("df_alt"), Alta)

        mensaje = """

        <div class="callout callout-success">
            <h4>Carga Exitosa</h4>
            <p>La data de activaciones y altas ha sido cargada con éxito</p>
        </div>

        <div class="container">

          <table class="table">
            <thead>
              <tr>
                <th class="text-center">Total Registros Activaciones cargadas</th>
                <th class="text-center">Sumatoria Total de Activaciones cargadas</th>
                <th class="text-center">Total Registros de Altas Cargadas</th>
                <th class="text-center">Sumatoria de Altas</th>
              </tr>
            </thead>
            <tbody>

              <tr class="info">
                <td class="text-center">%s</td>
                <td class="text-center">%s</td>
                <td class="text-center">%s</td>
                <td class="text-center">%s</td>
              </tr>

            </tbody>
          </table>
        </div>



            <div class = "col-md-2 col-lg-2 col-xs-2">
               <button type="button" class="btn btn-block btn-primary" onClick="goBack()" >
               Aceptar
               </button>
            </div>


            <script>
               function goBack() {
                   window.location=' http://10.160.8.96:8000/carga_data/';
                   }
            </script>

            """%(results_activaciones["count"] , int(results_activaciones["suma"]),
              results_altas["count"], results_altas["suma"])

        return render(request, "messages.html", {'message': mensaje})


    #uploader jerarquia_planes
    elif (validado==True and kwargs.get("reader")):

        uploader_jp(kwargs.get("reader"))
        mensaje = msj + """
            <div class = "col-md-2 col-lg-2 col-xs-2">
               <button type="button" class="btn btn-block btn-primary" onClick="goBack()" >
               Aceptar
               </button>
            </div>


            <script>
               function goBack() {
                   window.location=' http://10.160.8.96:8000/carga_data/';
                   }
            </script>"""

        return render(request, "messages.html", {'message': mensaje})

    #uploader bajas
    elif (validado==True and "df_baj" in kwargs.keys() ):

        uploader_bajas(kwargs.get("df_baj"))
        mensaje = """
            <div class="callout callout-success">
               <h4>Carga Exitosa</h4>
               <p>La data de Bajas ha sido cargada con éxito</p>
            </div>


            <div class = "col-md-2 col-lg-2 col-xs-2">
               <button type="button" class="btn btn-block btn-primary" onClick="goBack()" >
               Aceptar
               </button>
            </div>


            <script>
               function goBack() {
                   window.location=' http://10.160.8.96:8000/carga_data/';
                   }
            </script>

            """

        return render(request, "messages.html", {'message': mensaje})


    #uploader cuotas
    elif (validado==True and "df_cuota" in kwargs.keys() ):
        uploader_cuotas(kwargs.get("df_cuota"))
        mensaje = """
            <div class="callout callout-success">
               <h4>Carga Exitosa</h4>
               <p>La data de Cuotas ha sido cargada con éxito</p>
            </div>


            <div class = "col-md-2 col-lg-2 col-xs-2">
               <button type="button" class="btn btn-block btn-primary" onClick="goBack()" >
               Aceptar
               </button>
            </div>


            <script>
               function goBack() {
                   window.location=' http://10.160.8.96:8000/carga_data/';
                   }
            </script>

            """
        return render(request, "messages.html", {'message': mensaje})







def validator(request):
    validado=True


    if request.method == 'POST' and 'fj' in request.POST:
        mensaje = ""
        ruta_insumo = request.FILES.get('jerarquia')
        reader = pd.ExcelFile(ruta_insumo)
        ja=['Año', 'Mes', 'Código Agente', 'Código Sap', 'AA', 'Dirección', 'Región', 'Territorio', 'Zonificación', 'Ubicación CC / No CC', 'Estado', 'Gerente', 'Supervisor', 'Coordinador', 'Estatus', 'Dirección AA', 'Segmento', 'Territorio ICM', 'Región ICM', 'Zona ICM', 'Almacen Regional', 'Canal']
        jb=['Nombre CDS', 'Dirección', 'Gerente', 'Región', 'Territorio', 'Estado', 'Ubicación CC / No CC']
        jc=['Año', 'Mes', 'Código Plan', 'Nombre de Plan', 'Homologador de Planes', 'Renta Mensual por Plan', 'Recarga por Plan']

        #Validando nombre de hojas en Insumo
        if ('Inf Jerarquía Mensual' in reader.sheet_names) and ('Inf Jerarquía CDS' in reader.sheet_names) and ('Inf Homologador de Planes' in reader.sheet_names):
            dfa = pd.read_excel(reader, sheet_name='Inf Jerarquía Mensual')
            dfb = pd.read_excel(reader, sheet_name='Inf Jerarquía CDS')
            dfc = pd.read_excel(reader, sheet_name='Inf Homologador de Planes')

            #Validando Nombre y Orden de Columnas en Insumo
            if (ja == list(dfa)) and (jb == list(dfb)) and (jc == list(dfc)) :

                return go(request,True,"""
                    <div class="callout callout-success">
                        <h4>Carga Exitosa</h4>
                        <p>La data de la Jerarquia AA, ASI y CDS y Homologador de Planes ha sido cargada con éxito</p>
                    </div>""",reader=reader)



            else:
                return go(request,False,"""
                <div class="callout callout-danger">
                    <h4>Error de estructura de insumo</h4>
                    <p>Error en el orden o el nombre de las columnas.</p>
                    <p>Por favor valide el insumo, que el nombre y orden de las columnas sea correcto e intente nuevamente</p>
                </div>""")

        else:
            if bool(('Inf Jerarquía Mensual' in reader.sheet_names) == False):
                mensaje = mensaje + """
                <div class="callout callout-danger">
                    <h4>Error de estructura de insumo</h4>
                    <p>No se encontro la Hoja: "Inf Jerarquía Mensual" en el Excel, por favor valide el insumo e intente nuevamente</p>
                </div>
                """

            if bool(('Inf Jerarquía CDS' in reader.sheet_names) == False):
                mensaje = mensaje + """
                <div class="callout callout-danger">
                    <h4>Error de estructura de insumo</h4>
                    <p>No se encontro la Hoja: "Inf Jerarquía CDS" en el Excel, por favor valide el insumo e intente nuevamente</p>
                </div>
                """

            if bool(('Inf Homologador de Planes' in reader.sheet_names) == False):
                mensaje = mensaje + """
                <div class="callout callout-danger">
                    <h4>Error de estructura de insumo</h4>
                    <p>No se encontro la Hoja: "Inf Homologador de Planes" en el Excel, por favor valide el insumo e intente nuevamente</p>
                </div>
                """
            return go(request,False,mensaje)





    elif request.method == 'POST' and 'fa' in request.POST:

        ruta_activaciones = request.FILES.get('activaciones')
        ruta_altas = request.FILES.get('altas')

        columnas= ['Periodo', 'Fecha', 'Codigo Vendedor', 'Codigo Plan', 'Plataforma', 'Tecnologia', 'Tipo Equipo', 'Actividad', 'Canal']

        reader_activaciones = pd.ExcelFile(ruta_activaciones)
        reader_altas = pd.ExcelFile(ruta_altas)

        #Validando nombre de hojas en Insumo
        if ('Activaciones' in reader_activaciones.sheet_names) and ('Altas' in reader_altas.sheet_names):
            df_act = pd.read_excel(reader_activaciones, sheet_name='Activaciones')

            df_alt = pd.read_excel(reader_altas, sheet_name='Altas')
            df_alt["Fecha"] = pd.to_datetime(df_alt["Fecha"],format="%Y%m%d")



            #Validando Nombre y Orden de Columnas en Insumo
            if (columnas == list(df_act)) and (columnas == list(df_alt) ) :

                #Validando coincidencia de fechas de Activaciones y Altas
                #Toma la primera fila de periodo y compara
                if (df_act.loc[0,'Periodo'] == df_alt.loc[0,'Periodo']) == True:

                    df_act["Periodo"] = pd.to_datetime(df_act["Periodo"],format='%Y_%m')
                    df_alt["Periodo"] = pd.to_datetime(df_alt["Periodo"],format='%Y_%m')

                    #Validando contenido del insumo contra lo cargado anteriormente en Jerarquia
                    dfecha=df_act.loc[0,'Fecha']#Se lee la fecha de cualquier df para el QS1, los 2 deberian pertenecer al mismo mes

                    mes = dfecha.month
                    ano = dfecha.year

                    listBdCod=ProduccionPlan.objects.filter(fecha_prod__year=ano,
                    fecha_prod__month=mes).values_list('plan__codigo_plan',
                    flat=True).distinct().order_by()#QS1

                    listBdVi=Local.objects.values_list('codigo',flat=True).distinct().order_by()

                    listaPlanActivacion=list(df_act['Codigo Plan'].sort_values().unique())
                    listaPlanAltas=list(df_alt['Codigo Plan'].sort_values().unique())

                    listaCodigoAgenteAct=list(df_act['Codigo Vendedor'].sort_values().unique())
                    listaCodigoAgenteAlt=list(df_alt['Codigo Vendedor'].sort_values().unique())

                    mensaje=""
                    validado=True
                    for items in listaPlanActivacion:


                        if items not in listBdCod:
                            validado=False
                            m = """
                            <div class="callout callout-danger">
                               <h4>Error de Códigos de Plan</h4>
                               <p>El código del plan " %s " en el archivo Activacion No se encuentra en la jerarquía del mes cargado</p>
                            </div>

                            """%(items)
                            mensaje = mensaje + m


                    for items in listaPlanAltas:

                        if items not in listBdCod:
                            validado=False
                            m = """
                            <div class="callout callout-danger">
                               <h4>Error de Códigos de Plan</h4>
                               <p>El código del plan " %s " en el archivo Altas no se encuentra en la jerarquía del mes cargado</p>
                            </div>


                            """%(items)
                            mensaje = mensaje + m




                    for items in listaCodigoAgenteAct:

                        if items not in listBdVi:
                            validado=False
                            m = """
                            <div class="callout callout-danger">
                               <h4>Error de Códigos de Agente</h4>
                               <p>El código de agente " %s " en el archivo Activacion no se encuentra cargado en Base de Datos</p>
                               <p>Por favor valide la jerarquia e intente nuevamente</p>
                            </div>


                            """%(items)
                            mensaje = mensaje + m


                    for items in listaCodigoAgenteAlt:

                        if items not in listBdVi:
                            validado=False
                            m = """
                            <div class="callout callout-danger">
                               <h4>Error de Códigos de Agente</h4>
                               <p>El código de agente " %s " en el archivo Altas no se encuentra cargado en Base de Datos</p>
                               <p>Por favor valide la jerarquia e intente nuevamente</p>
                            </div>

                            """%(items)
                            mensaje = mensaje + m

                    #####################################################
                    return go(request, validado, mensaje, df_act = df_act, df_alt = df_alt) #nucleo
                    #####################################################





                else:
                    return go(request,False,"""
                        <div class="callout callout-danger">
                           <h4>Error de fecha</h4>
                           <p>Las fechas de las activaciones y altas no son iguales, por favor valide el insumo e intente nuevamente</p>
                        </div>""")



            else:
                return go(request,False,"""
                <div class="callout callout-danger">
                   <h4>Error de estructura de insumo</h4>
                   <p>Error en el orden o el nombre de las columnas, por favor valide el insumo e intente nuevamente</p>
                </div>""")


        else:
            return go(request,False,"""
                <div class="callout callout-danger">
                   <h4>Error de estructura de insumo</h4>
                   <p>Error en el nombre de las Hojas, verifique si las hojas existen y que tengan el nombre 'Activaciones' y 'Altas'
                   e intente nuevamente</p>
                </div>""")






    elif request.method == 'POST' and 'fba' in request.POST:


        ruta_bajas = request.FILES.get('bajas')
        ab= ['Periodo', 'Fecha', 'Codigo Vendedor', 'Codigo Plan', 'Plataforma', 'Tecnologia', 'Tipo Equipo', 'Brutas', 'Reactivados', 'Netas', 'Canal']
        reader_bajas = pd.ExcelFile(ruta_bajas)


        #Validando nombre de hojas en Insumo
        if 'Bajas' in reader_bajas.sheet_names:
            df_baj = pd.read_excel(reader_bajas, sheet_name='Bajas')
            df_baj["Periodo"] = pd.to_datetime(df_baj["Periodo"],format='%Y_%m')

            #Validando Nombre y Orden de Columnas en Insumo
            if  ab == list(df_baj):

                dfecha=df_baj.loc[0,'Periodo']

                listBdCod=ProduccionPlan.objects.filter(fecha_prod__year = dfecha.year,
                fecha_prod__month = dfecha.month).values_list('plan__codigo_plan',
                flat=True).distinct().order_by()

                listBdVi = Local.objects.values_list('codigo',flat=True).distinct().order_by()


                listaPlanBajas = list(df_baj['Codigo Plan'].sort_values().unique())


                listaCodigoAgenteBaj = list(df_baj['Codigo Vendedor'].sort_values().unique())


                validado = True
                mensaje=""
                for items in listaPlanBajas:

                    if items not in listBdCod:
                        validado=False
                        m = """
                        <div class="callout callout-danger">
                           <h4>Error de Códigos de Plan</h4>
                           <p>El código del plan " %s " en el archivo Bajas no se encuentra en la jerarquía del mes cargado</p>
                        </div>

                        """%(items)
                        mensaje = mensaje + m




                for items in listaCodigoAgenteBaj:

                    if items not in listBdVi:
                        validado=False
                        m = """
                        <div class="callout callout-danger">
                           <h4>Error de Códigos de Agente</h4>
                           <p>El código de agente " %s " en el archivo Bajas no se encuentra cargado en Base de Datos</p>
                           <p>Por favor valide la jerarquia e intente nuevamente</p>
                        </div>

                        """%(items)
                        mensaje = mensaje + m


                #############################
                return go(request, validado, mensaje, df_baj = df_baj)
                #############################





            else:
                return go(request,False,"""
                <div class="callout callout-danger">
                   <h4>Error de estructura de insumo</h4>
                   <p>Error en el orden o el nombre de las columnas, por favor valide el insumo e intente nuevamente</p>
                </div>""")




        else:
            return go(request,False,"""
                <div class="callout callout-danger">
                   <h4>Error de estructura de insumo</h4>
                   <p>Error en el nombre de la Hoja, verifique si la hoja existe y que tengan el nombre 'Bajas'
                   e intente nuevamente</p>
                </div>""")




    elif request.method == 'POST' and 'fcuota' in request.POST:
        """RECUERDA VALIDAR CAMPOS DEL ARCHIVO DE CUOTA"""
        reader_cuotas = pd.ExcelFile(request.FILES.get('cuotas'))

        columnas = ["Día", "Código de Venta", "Cuota Act. SP MP", "Cuota Act. SP ME",
        "Cuota Act. No SP MP", "Cuota Act. No SP ME", "Cuota TV HD", "Cuota TV SD",
        "Cuota Fijo",  "Cuota Cater SP MP",   "Cuota Cater SP ME",   "Cuota Cater No SP MP",
        "Cuota Cater No SP ME", "Cuota Altas SP MP",   "Cuota Altas SP ME",
        "Cuota Altas No SP MP",    "Cuota Altas No SP ME", "Cuota Act. SP Prepago",
        "Cuota Act. SP Pospago",   "Cuota Act. No SP Prepago",    "Cuota Act. No SP Pospago",
        "Cuota Altas SP Prepago", "Cuota Altas SP Pospago", "Cuota Altas No SP Prepago",
        "Cuota Altas No SP Pospago", "Cuota Act. Sp", "Cuota Act. No SP", "Cuota Act. Prepago",
        "Cuota Act. Pospago", "Cuota Altas Sp", "Cuota Altas No SP", "Cuota Altas Prepago",
        "Cuota Altas Pospago", "Cuota Activaciones Total", "Cuota Altas Total" ]

        if 'Cuota Diaria' in reader_cuotas.sheet_names:

            df_cuota = pd.read_excel(reader_cuotas,sheet_name='Cuota Diaria')
            print("Ya va a entrar a uploader_cuotas")
            mensaje=''

            #############################
            return go(request, validado, mensaje, df_cuota = df_cuota)
            #############################

        else:
            return go(request,False,"""
                <div class="callout callout-danger">
                   <h4>Error de estructura de insumo</h4>
                   <p>Error en el nombre de la Hoja, verifique si la hoja existe y que tengan el nombre 'Cuota Diaria'
                   e intente nuevamente</p>
                </div>""")






    else:
        fa = Actividades()
        fj = JerarquiaPlanes()
        fba = Bajas()
        fcuota = Cuotas()

        return render(request, "carga_data.html",{'fa': fa,'fj':fj, 'fba':fba, 'fcuota':fcuota})
