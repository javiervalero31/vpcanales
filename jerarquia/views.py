from django.shortcuts import render, redirect
import pandas as pd
from sqlalchemy import create_engine
from .forms import *
from .models import *
import json
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
import datetime, time
from dateutil.relativedelta import relativedelta
import calendar
from xlsxwriter.workbook import Workbook
import io
from urllib.request import urlopen
import ssl
from django.contrib.auth.models import User
from rest_framework import generics
from django.core.mail import send_mail
from django.template import loader
# engine pandas
engine = create_engine("mssql+pyodbc://sa:BaseSQL123@10.160.8.96:1433/vpcanales?driver=SQL+Server+Native+Client+11.0")


#Serializa La respuesta para el AJAX
def jerarquia_serializer(i):
    return {'codigo':i.get('codigo_unico'),'nombre':i.get('nombre_key__nombre'),'lider': i.get('lider_key__lider')}

#Renderiza el filtro y Realiza la consulta AJAX y recibe la solicitud de aprobacion
def jerarquia(request):
    fil = filtro()
    user_group = list(request.user.groups.values_list('name', flat=True))

    if 'Aprobador Final' in user_group: user_group.remove('Aprobador Final')
    if 'Gerente' in user_group: user_group.remove('Gerente')
    if 'Lider' in user_group: user_group.remove('Lider')
    if 'Coordinador' in user_group: user_group.remove('Coordinador')
    user_group = ''.join(map(str,user_group))
    fil.fields['lider'].queryset = Lider.objects.filter(lider__in=(Temporal.objects.filter(region_key__region=user_group).values('lider_key__lider').distinct())).distinct().order_by('lider')
    print(Temporal.objects.filter(region_key__region=user_group).values('lider_key__lider'))
    #Crea solicitud
    if request.method == "POST" and 'solicitud' in request.POST:
        codigo = request.POST.get("codigo_unico")
        if Cambio.objects.filter(Q(Q(codigo_unico=codigo)& Q(aprobacion_1__isnull=True) & Q(rechazado__isnull=True))|
                              Q(Q(codigo_unico=codigo) & Q(aprobacion_1__isnull=True) & Q(aprobacion_2__isnull=True) & Q(rechazado__isnull=True))).exists():
            return render(request,"messages.html",{'message':'Solicitud ya existe'})
        elif datetime.datetime.today().day > calendar.monthrange(datetime.datetime.today().year,datetime.datetime.today().month)[1] +20:
            return render(request,"messages.html",{'message':'Ya no se admiten mas modificaciones'})
        else:
            if solicitar_modificacion(request):
                return render(request,"messages.html",{'message':'Solicitud Exitosa'})
            else:
                return render(request,"messages.html",{'message':'Error en los datos ingresados para la solicitud'})
        return redirect('jerarquia')
    #Aprobacion de Solicitud


    if request.method == "POST":
        params= {}
        user_group = list(request.user.groups.values_list('name', flat=True))

        if 'Aprobador Final' in user_group: user_group.remove('Aprobador Final')
        if 'Gerente' in user_group: user_group.remove('Gerente')
        if 'Lider' in user_group: user_group.remove('Lider')
        if 'Coordinador' in user_group: user_group.remove('Coordinador')
        user_group = ''.join(map(str,user_group))
        params['region_key__region'] = user_group
        if request.POST.get("tipo") != '':
            params['tipo_key__tipo'] = request.POST.get("tipo")
        # if request.POST.get("region") != '':
        #     params['region_key__region'] = request.POST.get("region")
        if request.POST.get("lider") != '':
            params['lider_key__lider'] = request.POST.get("lider")
        if request.POST.get("codigo") != '':
            params['codigo_unico'] = request.POST.get("codigo")
        consulta = Temporal.objects.filter(**params).values('nombre_key__nombre',
                                                             'codigo_unico',
                                                             'lider_key__lider')

        consulta = [jerarquia_serializer(i) for i in consulta]

        return JsonResponse(consulta, safe=False)

    return render(request, "jerarquia.html",{'filtro':fil})

#Renderiza la modal, consulta el codigo unico y muestra los valores actuales de Temporal
def consulta_codigo(request,codigo_unico):
    nombre = Temporal.objects.filter(codigo_unico = codigo_unico).values('nombre_key__nombre').values_list('nombre_key__nombre', flat=True)
    nombre = nombre[0] +chr(10) +codigo_unico
    consulta = Temporal.objects.get(codigo_unico = codigo_unico)
    form = editar(request.POST or None, instance=consulta)
    solicitar = '<input type="submit" value="Solicitar" class="btn btn-block btn-primary" name="solicitud">'
    return render(request, "jerarquia_editar.html",{'form':form,'solicitar':solicitar, 'nombre':nombre})

#Crea el registro de Cambio para posterior aprobacion
def solicitar_modificacion(request):

    if 'enero' in request.POST:
        enero = True
    else:
        enero = False
    if 'febrero' in request.POST:
        febrero = True
    else:
        febrero = False

    if 'marzo' in request.POST:
        marzo = True
    else:
        marzo = False
    if 'abril' in request.POST:
        abril = True
    else:
        abril = False
    if 'mayo' in request.POST:
        mayo = True
    else:
        mayo = False
    if 'junio' in request.POST:
        junio = True
    else:
        junio = False
    if 'julio' in request.POST:
        julio = True
    else:
        julio = False
    if 'agosto' in request.POST:
        agosto = True
    else:
        agosto = False
    if 'septiembre' in request.POST:
        septiembre = True
    else:
        septiembre = False
    if 'octubre' in request.POST:
        octubre = True
    else:
        octubre = False
    if 'noviembre' in request.POST:
        noviembre = True
    else:
        noviembre = False
    if 'diciembre' in request.POST:
        diciembre = True
    else:
        diciembre = False
    form = editar(request.POST)
    if form.is_valid():
        Cambio(a000sap=request.POST.get("a000sap"),
             codigo_unico=request.POST.get("codigo_unico"),
             visitas=request.POST.get("visitas"),
             enero=enero,
             febrero=febrero,
             marzo=marzo,
             abril=abril,
             mayo=mayo,
             junio=junio,
             julio=julio,
             agosto=agosto,
             septiembre=septiembre,
             octubre=octubre,
             noviembre=noviembre,
             diciembre=diciembre,
             latitud=request.POST.get("latitud"),
             longitud=request.POST.get("longitud"),
             direccion_fisica=request.POST.get("direccion_fisica"),
             direccion_fiscal=request.POST.get("direccion_fiscal"),
             persona_contacto=request.POST.get("persona_contacto"),
             correo_tienda=request.POST.get("correo_tienda"),
             correo_empresario=request.POST.get("correo_empresario"),
             telefono_tienda=request.POST.get("telefono_tienda"),
             telefono_empresario=request.POST.get("telefono_empresario"),
             hora_apertura=request.POST.get("hora_apertura"),
             hora_cierre=request.POST.get("hora_cierre"),
             empleados=request.POST.get("empleados"),
             caso_remedy=request.POST.get("caso_remedy"),
             estado_key=form.cleaned_data["estado_key"],
             municipio_key=form.cleaned_data["municipio_key"],
             tipo_key=form.cleaned_data["tipo_key"],
             tipo_aa_key=form.cleaned_data["tipo_aa_key"],
             oficina_key=form.cleaned_data["oficina_key"],
             codigo_deudor_key=form.cleaned_data["codigo_deudor_key"],
             nombre_key=form.cleaned_data["nombre_key"],
             direccion_key=form.cleaned_data["direccion_key"],
             region_key=form.cleaned_data["region_key"],
             coordinador_key=form.cleaned_data["coordinador_key"],
             lider_key=form.cleaned_data["lider_key"],
             gerente_key=form.cleaned_data["gerente_key"],
             centro_recarga_key=form.cleaned_data["centro_recarga_key"],
             distribuidor_key=form.cleaned_data["distribuidor_key"],
             status_key=form.cleaned_data["status_key"],
             rif_key=form.cleaned_data["rif_key"],
             punto_rojo=form.cleaned_data["punto_rojo"],
             aprobacion_1 = None, aprobacion_2= None,
             rechazado = None,
             idop_solicitante=request.user.get_username()).save()
        return True
    else:
        print("Errores ----> ",form.errors) #JV
        return False

#Renderiza los cambios pendientes
def aprobar(request):
    grupo_solicitante = list(User.objects.filter(username__in=Cambio.objects.filter(aprobacion_1__isnull=True,
                                                                           aprobacion_2__isnull=True,
                                                                           rechazado__isnull=True).values('idop_solicitante')).values_list('groups__name'))
    grupo_gerente = list(request.user.groups.values_list('name', flat=True))
    grupo = False
    if set(grupo_solicitante).isdisjoint(grupo_gerente):
        grupo = True
    if request.method == "POST" and 'aprobacion' in request.POST:
        codigo = request.POST.get("codigo_unico")
        cambio = Cambio.objects.get((Q(codigo_unico=codigo)&Q(aprobacion_1=None, rechazado=None)|Q(codigo_unico=codigo)&Q(aprobacion_2=None)&Q(rechazado=None))).__dict__

        if Cambio.objects.filter(aprobacion_1__isnull=False,codigo_unico=codigo, aprobacion_2=None):
            solicitante = Cambio.objects.filter(codigo_unico=codigo,aprobacion_1__isnull=False, aprobacion_2=None).values('idop_solicitante')
            Cambio.objects.filter(codigo_unico=codigo,aprobacion_1__isnull=False, aprobacion_2=None).update(aprobacion_2=request.user.get_username())
            Temporal.objects.filter(codigo_unico=codigo).update(a000sap=cambio.get('a000sap'),
                                                                    codigo_unico=cambio.get('codigo_unico'),
                                                                    visitas=cambio.get('visitas'),
                                                                    latitud=cambio.get('latitud'),
                                                                    longitud=cambio.get('longitud'),
                                                                    direccion_fisica=cambio.get('direccion_fisica'),
                                                                    direccion_fiscal=cambio.get('direccion_fiscal'),
                                                                    persona_contacto=cambio.get('persona_contacto'),
                                                                    correo_tienda=cambio.get('correo_tienda'),
                                                                    correo_empresario=cambio.get('correo_empresario'),
                                                                    telefono_empresario=cambio.get('telefono_empresario'),
                                                                    telefono_tienda=cambio.get('telefono_tienda'),
                                                                    hora_apertura=cambio.get('hora_apertura'),
                                                                    hora_cierre=cambio.get('hora_cierre'),
                                                                    empleados=cambio.get('empleados'),
                                                                    punto_rojo=cambio.get('punto_rojo'),
                                                                    caso_remedy=cambio.get('caso_remedy'),
                                                                    enero=cambio.get('enero'),
                                                                    febrero=cambio.get('febrero'),
                                                                    marzo=cambio.get('marzo'),
                                                                    abril=cambio.get('abril'),
                                                                    mayo=cambio.get('mayo'),
                                                                    junio=cambio.get('junio'),
                                                                    julio=cambio.get('julio'),
                                                                    agosto=cambio.get('agosto'),
                                                                    septiembre=cambio.get('septiembre'),
                                                                    octubre=cambio.get('octubre'),
                                                                    noviembre=cambio.get('noviembre'),
                                                                    diciembre=cambio.get('diciembre'),
                                                                    estado_key=cambio.get('estado_key_id'),
                                                                    municipio_key=cambio.get('municipio_key_id'),
                                                                    tipo_key=cambio.get('tipo_key_id'),
                                                                    tipo_aa_key=cambio.get('tipo_aa_key_id'),
                                                                    oficina_key=cambio.get('oficina_key_id'),
                                                                    codigo_deudor_key=cambio.get('codigo_deudor_key_id'),
                                                                    nombre_key=cambio.get('nombre_key_id'),
                                                                    direccion_key=cambio.get('direccion_key_id'),
                                                                    region_key=cambio.get('region_key_id'),
                                                                    coordinador_key=cambio.get('coordinador_key_id'),
                                                                    lider_key=cambio.get('lider_key_id'),
                                                                    gerente_key=cambio.get('gerente_key_id'),
                                                                    centro_recarga_key=cambio.get('centro_recarga_key_id'),
                                                                    distribuidor_key=cambio.get('distribuidor_key_id'),
                                                                    status_key=cambio.get('status_key_id'),
                                                                    rif_key=cambio.get('rif_key_id'))
            html_message = loader.render_to_string(
                    "jerarquia_mail.html", {'codigo':codigo,'estado':'aprobado'}
                )
            send_mail('Gestor de Jerarquia', '', 'GciaAnaliticaComercial.ve@telefonica.com',list(User.objects.filter(username=solicitante).values_list('email', flat=True)), fail_silently=False,html_message=html_message)
        if Cambio.objects.filter(codigo_unico=codigo, aprobacion_1=None, aprobacion_2=None):
            Cambio.objects.filter(codigo_unico=codigo, aprobacion_1=None, aprobacion_2=None, rechazado=None).update(aprobacion_1=request.user.get_username())


    if request.method == "POST" and 'rechazo' in request.POST:
        solicitante = Cambio.objects.filter(codigo_unico=codigo,aprobacion_1__isnull=False, aprobacion_2=None).values('idop_solicitante')
        codigo = request.POST.get("codigo_unico")
        grupo_rechazo = list(request.user.groups.values_list('name', flat=True))
        if 'Gerente' in grupo_rechazo:
            Cambio.objects.filter(codigo_unico=codigo, aprobacion_1__isnull=True).update(rechazado=request.user.get_username())
            html_message = loader.render_to_string(
                    "jerarquia_mail.html", {'codigo':codigo,'estado':'rechazado'}
                )
            send_mail('Gestor de Jerarquia', '', 'GciaAnaliticaComercial.ve@telefonica.com',list(User.objects.filter(username=solicitante).values_list('email', flat=True)), fail_silently=False,html_message=html_message)
        if 'Aprobador Final' in grupo_rechazo:
            Cambio.objects.filter(codigo_unico=codigo, aprobacion_2__isnull=True).update(rechazado=request.user.get_username())
            html_message = loader.render_to_string(
                    "jerarquia_mail.html", {'codigo':codigo,'estado':'rechazado'}
                )
        if 'Gerente' in request.user.groups.values_list('name',flat=True):
            consulta = Cambio.objects.filter(aprobacion_1=None,rechazado=None).values('nombre_key__nombre',
                                                                                  'codigo_unico',
                                                                                  'lider_key__lider')

        return render(request, "jerarquia_aprobar.html", {'results':consulta})

    elif 'Aprobador Final' in request.user.groups.values_list('name',flat=True):
        consulta = Cambio.objects.filter(aprobacion_1__isnull=False,aprobacion_2__isnull=True,rechazado__isnull=True).values('nombre_key__nombre',
                                                             'codigo_unico',
                                                             'lider_key__lider')
        return render(request, "jerarquia_aprobar.html", {'results':consulta})
    elif ('Gerente' in request.user.groups.values_list('name',flat=True)) and (grupo):

        usuario_conectado = request.user.username
        consulta = Cambio.objects.filter(Q(aprobacion_1__isnull=True)&
                                 Q(aprobacion_2__isnull=True)&
                                 Q(rechazado__isnull=True)&
                                 Q(idop_solicitante__in=User.objects.filter(username__iexact=usuario_conectado).values_list('groups__user__username'))).values('nombre_key__nombre',
                                                                                      'codigo_unico',
                                                                                      'lider_key__lider')
        return render(request, "jerarquia_aprobar.html", {'results':consulta})
    else:
        return render(request, "jerarquia_aprobar.html", {})

#Renderiza la modal para aprobar cambios(muestra el registro original y el cambio)
def consulta_cambio(request, codigo_unico):
    original = Temporal.objects.get(codigo_unico = codigo_unico)
    solicitud = Cambio.objects.get(Q(codigo_unico = codigo_unico)&Q(Q(aprobacion_1__isnull=True)|Q(aprobacion_2__isnull=True))&Q(rechazado__isnull=True))

    form_original = aprobar_original(request.POST or None, instance=original)
    form_cambio = aprobar_cambio(request.POST or None, instance=solicitud)
    submit = 'aprobacion'
    aprobar = '<input type="submit" value="Aprobar Cambio" class="btn btn-block btn-primary" name="aprobacion" style = "width:200px">'
    rechazar = '<input type="submit" value="Rechazar Cambio" class="btn btn-danger" name="rechazo" style = "width:200px">'

    return render(request, "jerarquia_editar.html",{'original':form_original,'cambio':form_cambio,'rechazo':rechazar,'aprobar':aprobar})

#Pasa la jerarquia al historico
def cerrar_jerarquia(request):
    temporal = Temporal.objects.all()

    ahora = datetime.datetime.now()+ relativedelta(months=1)
    ahora = ahora.strftime("%Y-%m")+'-01'
    Historico.objects.filter(fecha=ahora).delete()
    for objects in temporal:
        a = objects.__dict__
        a.pop('id')
        a.pop('_state')
        a['fecha']= ahora
        Historico.objects.create(**a)
    # temporal.pop('id')



    return render(request, "messages.html", {'message':'Jerarquia Cerrada Exitosamente'})

#Descargar jerarquia no cerrada
def descarga_especial(request):
    query = """select
    tipo,
    status,
    codigo_unico,
    a000sap,
    codigo_deudor,
    nombre,
    direccion,
    region,
    gerente,
    lider,
    coordinador,
    direccion_fiscal,
    direccion_fisica,
    latitud,
    longitud,
    case
    when punto_rojo = 1 then 'SI'
    when punto_rojo = 0 then 'NO'
    end as punto_rojo,
    oficina,
    rif,
    tipo_aa,
    Estado,
    municipio,
    case
    when enero = 1 then 'SI'
    when enero = 0 then 'NO'
    end as enero,
    case
    when febrero = 1 then 'SI'
    when febrero = 0 then 'NO'
    end as febrero,
    case
    when marzo = 1 then 'SI'
    when marzo = 0 then 'NO'
    end as marzo,
    case
    when abril = 1 then 'SI'
    when abril = 0 then 'NO'
    end as abril,
    case
    when mayo = 1 then 'SI'
    when mayo = 0 then 'NO'
    end as mayo,
    case
    when Junio = 1 then 'SI'
    when Junio = 0 then 'NO'
    end as Junio,
    case
    when julio = 1 then 'SI'
    when julio = 0 then 'NO'
    end as julio,
    case
    when agosto = 1 then 'SI'
    when agosto = 0 then 'NO'
    end as agosto,
    case
    when septiembre = 1 then 'SI'
    when septiembre = 0 then 'NO'
    end as septiembre,
    case
    when octubre = 1 then 'SI'
    when octubre = 0 then 'NO'
    end as octubre,
    case
    when noviembre = 1 then 'SI'
    when noviembre = 0 then 'NO'
    end as noviembre,
    case
    when diciembre = 1 then 'SI'
    when diciembre = 0 then 'NO'
    end as diciembre,
    persona_contacto,
    correo_tienda,
    correo_empresario,
    telefono_tienda,
    telefono_empresario,
    hora_apertura,
    hora_cierre,
    empleados,
    caso_remedy,
    centro_recarga,
    distribuidor
    from jerarquia_temporal h
    left join jerarquia_centrorecarga cr on cr.id = h.centro_recarga_key_id
    left join jerarquia_codigodeudor cd on cd.id = h.codigo_deudor_key_id
    inner join jerarquia_coordinador co on co.id = h.coordinador_key_id
    left join jerarquia_direccion di on di.id = h.direccion_key_id
    left join jerarquia_distribuidor dt on dt.id = h.distribuidor_key_id
    inner join jerarquia_gerente g on g.id = h.gerente_key_id
    inner join jerarquia_lider l on l.id = h.lider_key_id
    inner join jerarquia_nombre n on n.id = h.nombre_key_id
    left join jerarquia_oficina o on o.id = h.oficina_key_id
    inner join jerarquia_region r on r.id = h.region_key_id
    inner join jerarquia_rif rif on rif.id = h.rif_key_id
    left join jerarquia_tipoaa aa on aa.id = h.tipo_aa_key_id
    inner join jerarquia_tipo t on t.id = h.tipo_key_id
    left join jerarquia_status st on st.id = h.status_key_id
    left join jerarquia_municipios mu on mu.id_municipio = h.municipio_key_id
    inner join jerarquia_estados es on es.id_estado = mu.id_estado"""
    data = pd.read_sql_query(query, engine)
    data=data.rename(columns={'codigo_unico':'Codigo Unico',
                              'a000sap':'A000SAP',
                              'codigo_deudor':'Codigo Deudor',
                              'nombre':'Nombre',
                              'tipo':'Tipo',
                              'latitud':'Latitud',
                              'longitud':'Longitud',
                              'direccion_fiscal':'Direccion Fiscal',
                              'direccion_fisica':'Direccion Fisica',
                              'persona_contacto':'Persona Contacto',
                              'correo_tienda':'Correo Tienda',
                              'correo_empresario':'Correo Empresario',
                              'telefono_tienda':'Telefono Tienda',
                              'telefono_empresario':'Telefono Empresario',
                              'hora_apertura':'Hora Apertura',
                              'hora_cierre':'Hora Cierre',
                              'empleados':'Empleados',
                              'punto_rojo':'Punto Rojo',
                              'caso_remedy':'Caso Remedy',
                              'centro_recarga':'Centro Recarga',
                              'direccion':'Direccion',
                              'distribuidor':'Distribuidor',
                              'gerente':'Gerente',
                              'lider':'Lider',
                              'coordinador':'Coordinador',
                              'oficina':'Oficina',
                              'region':'Region',
                              'rif':'RIF',
                              'status':'Status',
                              'tipo_aa':'Tipo AA',
                              'municipio':'Municipio',
                              'enero':'Visita Enero',
                              'febrero':'Visita Febrero',
                              'marzo':'Visita Marzo',
                              'abril':'Visita Abril',
                              'mayo':'Visita Mayo',
                              'junio':'Visita Junio',
                              'julio':'Visita Julio',
                              'agosto':'Visita Agosto',
                              'septiembre':'Visita Septiembre',
                              'octubre':'Visita Octubre',
                              'noviembre':'Visita Noviembre',
                              'diciembre':'Visita Diciembre'})
    out= io.BytesIO()
    writer = pd.ExcelWriter(out,engine='xlsxwriter')
    writer.book.filename = out
    data.to_excel(writer,sheet_name="Jerarquia", index=False, startrow=4)
    workbook = writer.book
    worksheet = writer.sheets["Jerarquia"]
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
    date_format = workbook.add_format({'num_format': 'hh:mm'})
    worksheet.set_column('AL:AM', 9, date_format)

    worksheet.write("D1","Vicepresidencia de Canales")
    worksheet.write("D2","Direccion de Planificacion de Canales")
    worksheet.write("D3","Gerencia de Analitica de Canales")

    for col_num, value in enumerate(data.columns.values):
        worksheet.write(4, col_num, value, header_format)
    worksheet.set_column('A:Z',13)
    writer.save()
    out.seek(0)
    response = HttpResponse(out.read(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = "attachment; filename='Jerarquia.xlsx'"
    return response

#Se descarga la jerarquia del mes seleccionado
def descarga_jerarquia(request):
    import locale
    locale.setlocale(locale.LC_TIME,'')
    if request.method == "POST":
        fecha = request.POST.get("fecha")
        fecha = datetime.datetime.strptime(fecha, '%d de %B de %Y')
        query = """
        select
        tipo,
        status,
        codigo_unico,
        a000sap,
        codigo_deudor,
        nombre,
        direccion,
        region,
        gerente,
        lider,
        coordinador,
        direccion_fiscal,
        direccion_fisica,
        latitud,
        longitud,
        case
        when punto_rojo = 1 then 'SI'
        when punto_rojo = 0 then 'NO'
        end as punto_rojo,
        oficina,
        rif,
        tipo_aa,
        Estado,
        municipio,
        case
        when enero = 1 then 'SI'
        when enero = 0 then 'NO'
        end as enero,
        case
        when febrero = 1 then 'SI'
        when febrero = 0 then 'NO'
        end as febrero,
        case
        when marzo = 1 then 'SI'
        when marzo = 0 then 'NO'
        end as marzo,
        case
        when abril = 1 then 'SI'
        when abril = 0 then 'NO'
        end as abril,
        case
        when mayo = 1 then 'SI'
        when mayo = 0 then 'NO'
        end as mayo,
        case
        when Junio = 1 then 'SI'
        when Junio = 0 then 'NO'
        end as Junio,
        case
        when julio = 1 then 'SI'
        when julio = 0 then 'NO'
        end as julio,
        case
        when agosto = 1 then 'SI'
        when agosto = 0 then 'NO'
        end as agosto,
        case
        when septiembre = 1 then 'SI'
        when septiembre = 0 then 'NO'
        end as septiembre,
        case
        when octubre = 1 then 'SI'
        when octubre = 0 then 'NO'
        end as octubre,
        case
        when noviembre = 1 then 'SI'
        when noviembre = 0 then 'NO'
        end as noviembre,
        case
        when diciembre = 1 then 'SI'
        when diciembre = 0 then 'NO'
        end as diciembre,
        persona_contacto,
        correo_tienda,
        correo_empresario,
        telefono_tienda,
        telefono_empresario,
        hora_apertura,
        hora_cierre,
        empleados,
        caso_remedy,
        centro_recarga,
        distribuidor
        from jerarquia_historico h
        left join jerarquia_centrorecarga cr on cr.id = h.centro_recarga_key_id
        left join jerarquia_codigodeudor cd on cd.id = h.codigo_deudor_key_id
        inner join jerarquia_coordinador co on co.id = h.coordinador_key_id
        left join jerarquia_direccion di on di.id = h.direccion_key_id
        left join jerarquia_distribuidor dt on dt.id = h.distribuidor_key_id
        inner join jerarquia_gerente g on g.id = h.gerente_key_id
        inner join jerarquia_lider l on l.id = h.lider_key_id
        inner join jerarquia_nombre n on n.id = h.nombre_key_id
        left join jerarquia_oficina o on o.id = h.oficina_key_id
        inner join jerarquia_region r on r.id = h.region_key_id
        inner join jerarquia_rif rif on rif.id = h.rif_key_id
        left join jerarquia_tipoaa aa on aa.id = h.tipo_aa_key_id
        inner join jerarquia_tipo t on t.id = h.tipo_key_id
        left join jerarquia_status st on st.id = h.status_key_id
        left join jerarquia_municipios mu on mu.id_municipio = h.municipio_key_id
        inner join jerarquia_estados es on es.id_estado = mu.id_estado
        where fecha='%s'"""%(fecha)
        data = pd.read_sql_query(query, engine)
        data=data.rename(columns={'codigo_unico':'Codigo Unico',
                                  'a000sap':'A000SAP',
                                  'codigo_deudor':'Codigo Deudor',
                                  'nombre':'Nombre',
                                  'tipo':'Tipo',
                                  'latitud':'Latitud',
                                  'longitud':'Longitud',
                                  'direccion_fiscal':'Direccion Fiscal',
                                  'direccion_fisica':'Direccion Fisica',
                                  'persona_contacto':'Persona Contacto',
                                  'correo_tienda':'Correo Tienda',
                                  'correo_empresario':'Correo Empresario',
                                  'telefono_tienda':'Telefono Tienda',
                                  'telefono_empresario':'Telefono Empresario',
                                  'hora_apertura':'Hora Apertura',
                                  'hora_cierre':'Hora Cierre',
                                  'empleados':'Empleados',
                                  'punto_rojo':'Punto Rojo',
                                  'caso_remedy':'Caso Remedy',
                                  'centro_recarga':'Centro Recarga',
                                  'direccion':'Direccion',
                                  'distribuidor':'Distribuidor',
                                  'gerente':'Gerente',
                                  'lider':'Lider',
                                  'coordinador':'Coordinador',
                                  'oficina':'Oficina',
                                  'region':'Region',
                                  'rif':'RIF',
                                  'status':'Status',
                                  'tipo_aa':'Tipo AA',
                                  'municipio':'Municipio',
                                  'enero':'Visita Enero',
                                  'febrero':'Visita Febrero',
                                  'marzo':'Visita Marzo',
                                  'abril':'Visita Abril',
                                  'mayo':'Visita Mayo',
                                  'junio':'Visita Junio',
                                  'julio':'Visita Julio',
                                  'agosto':'Visita Agosto',
                                  'septiembre':'Visita Septiembre',
                                  'octubre':'Visita Octubre',
                                  'noviembre':'Visita Noviembre',
                                  'diciembre':'Visita Diciembre'})





        out= io.BytesIO()
        writer = pd.ExcelWriter(out,engine='xlsxwriter')
        writer.book.filename = out
        data.to_excel(writer,sheet_name="Jerarquia", index=False, startrow=4)
        workbook = writer.book
        worksheet = writer.sheets["Jerarquia"]
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
        date_format = workbook.add_format({'num_format': 'hh:mm'})
        worksheet.set_column('AL:AM', 9, date_format)
        worksheet.write("D1","Vicepresidencia de Canales")
        worksheet.write("D2","Direccion de Planificacion de Canales")
        worksheet.write("D3","Gerencia de Analitica de Canales")
        format_fecha = workbook.add_format({'num_format': 'dd/mm/yy'})
        worksheet.write("G2",fecha,format_fecha)


        for col_num, value in enumerate(data.columns.values):
            worksheet.write(4, col_num, value, header_format)
        worksheet.set_column('A:Z',13)
        writer.save()
        out.seek(0)
        response = HttpResponse(out.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = "attachment; filename='Jerarquia.xlsx'"
        return response

    form = descarga()

    return render(request,"jerarquia_descarga.html", {'form':form})

def formularios_vista_aprobador(request):
    formularios = agregar_valores()
    mensaje = """<div class="alert alert-warning alert-dismissible">
                <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                <h4><i class="icon fa fa-warning"></i> Atento</h4>
                Recuerda que la informacion que ingreses en estos campos quedara PERMANENTEMENTE grabada en base de datos.<br/>
                Verifique dos veces antes de hacer click en agregar.
              </div>"""
    if request.method == 'POST' and 'tipo' in request.POST:
        tipo = request.POST.getlist('tipo')[0]
        Tipo(tipo=tipo,ldap=User.objects.get(username=request.user)).save()
        mensaje = """<div class="alert alert-success alert-dismissible">
                <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                <h4><i class="icon fa fa-check"></i> Exito!</h4>
                El valor de Tipo se acaba de agregar con exito a la base de datos.
              </div>"""
        return render(request, "jerarquia_vista_aprobador.html", {'mensaje':mensaje})

    if request.method == 'POST' and 'tipo_aa' in request.POST:
        tipo_aa = request.POST.getlist('tipo_aa')[0]
        TipoAa(tipo_aa=tipo_aa,ldap=User.objects.get(username=request.user)).save()
        mensaje = """<div class="alert alert-success alert-dismissible">
                <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                <h4><i class="icon fa fa-check"></i> Exito!</h4>
                El valor de Tipo AA se acaba de agregar con exito a la base de datos.
              </div>"""
        return render(request, "jerarquia_vista_aprobador.html", {'mensaje':mensaje})

    if request.method == 'POST' and 'oficina' in request.POST:
        oficina = request.POST.getlist('oficina')[0]
        Oficina(oficina=oficina,ldap=User.objects.get(username=request.user)).save()
        mensaje = """<div class="alert alert-success alert-dismissible">
                <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                <h4><i class="icon fa fa-check"></i> Exito!</h4>
                El valor de Oficina se acaba de agregar con exito a la base de datos.
              </div>"""
        return render(request, "jerarquia_vista_aprobador.html", {'mensaje':mensaje})

    if request.method == 'POST' and 'rif' in request.POST:
        rif = request.POST.getlist('rif')[0]
        Rif(rif=rif,ldap=User.objects.get(username=request.user)).save()
        mensaje = """<div class="alert alert-success alert-dismissible">
                <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                <h4><i class="icon fa fa-check"></i> Exito!</h4>
                El valor de Rif se acaba de agregar con exito a la base de datos.
              </div>"""
        return render(request, "jerarquia_vista_aprobador.html", {'mensaje':mensaje})

    if request.method == 'POST' and 'codigo_deudor' in request.POST:
        codigo_deudor = request.POST.getlist('codigo_deudor')[0]
        CodigoDeudor(codigo_deudor=codigo_deudor,ldap=User.objects.get(username=request.user)).save()
        mensaje = """<div class="alert alert-success alert-dismissible">
                <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                <h4><i class="icon fa fa-check"></i> Exito!</h4>
                El valor de Codigo Deudor se acaba de agregar con exito a la base de datos.
              </div>"""
        return render(request, "jerarquia_vista_aprobador.html", {'mensaje':mensaje})

    if request.method == 'POST' and 'nombre' in request.POST:
        nombre = request.POST.getlist('nombre')[0]
        Nombre(nombre=nombre,ldap=User.objects.get(username=request.user)).save()
        mensaje = """<div class="alert alert-success alert-dismissible">
                <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                <h4><i class="icon fa fa-check"></i> Exito!</h4>
                El valor de Nombre se acaba de agregar con exito a la base de datos.
              </div>"""
        return render(request, "jerarquia_vista_aprobador.html", {'mensaje':mensaje})

    if request.method == 'POST' and 'direccion' in request.POST:
        direccion = request.POST.getlist('direccion')[0]
        Direccion(direccion=direccion,ldap=User.objects.get(username=request.user)).save()
        mensaje = """<div class="alert alert-success alert-dismissible">
                <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                <h4><i class="icon fa fa-check"></i> Exito!</h4>
                El valor de Direccion se acaba de agregar con exito a la base de datos.
              </div>"""
        return render(request, "jerarquia_vista_aprobador.html", {'mensaje':mensaje})

    if request.method == 'POST' and 'region' in request.POST:
        region = request.POST.getlist('region')[0]
        Region(region=region,ldap=User.objects.get(username=request.user)).save()
        mensaje = """<div class="alert alert-success alert-dismissible">
                <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                <h4><i class="icon fa fa-check"></i> Exito!</h4>
                El valor de Region se acaba de agregar con exito a la base de datos.
              </div>"""
        return render(request, "jerarquia_vista_aprobador.html", {'mensaje':mensaje})

    if request.method == 'POST' and 'gerente' in request.POST:
        gerente = request.POST.getlist('gerente')[0]
        Gerente(gerente=gerente,ldap=User.objects.get(username=request.user)).save()
        mensaje = """<div class="alert alert-success alert-dismissible">
                <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                <h4><i class="icon fa fa-check"></i> Exito!</h4>
                El valor de Gerente se acaba de agregar con exito a la base de datos.
              </div>"""
        return render(request, "jerarquia_vista_aprobador.html", {'mensaje':mensaje})

    if request.method == 'POST' and 'lider' in request.POST:
        lider = request.POST.getlist('lider')[0]
        Lider(lider=lider,ldap=User.objects.get(username=request.user)).save()
        mensaje = """<div class="alert alert-success alert-dismissible">
                <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                <h4><i class="icon fa fa-check"></i> Exito!</h4>
                El valor de Lider se acaba de agregar con exito a la base de datos.
              </div>"""
        return render(request, "jerarquia_vista_aprobador.html", {'mensaje':mensaje})

    if request.method == 'POST' and 'coordinador' in request.POST:
        coordinador = request.POST.getlist('coordinador')[0]
        Coordinador(coordinador=coordinador,ldap=User.objects.get(username=request.user)).save()
        mensaje = """<div class="alert alert-success alert-dismissible">
                <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                <h4><i class="icon fa fa-check"></i> Exito!</h4>
                El valor de Coordinador se acaba de agregar con exito a la base de datos.
              </div>"""
        return render(request, "jerarquia_vista_aprobador.html", {'mensaje':mensaje})

    if request.method == 'POST' and 'centro_recarga' in request.POST:
        centro_recarga = request.POST.getlist('centro_recarga')[0]
        CentroRecarga(centro_recarga=centro_recarga,ldap=User.objects.get(username=request.user)).save()
        mensaje = """<div class="alert alert-success alert-dismissible">
                <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                <h4><i class="icon fa fa-check"></i> Exito!</h4>
                El valor de Centro de Recarga se acaba de agregar con exito a la base de datos.
              </div>"""
        return render(request, "jerarquia_vista_aprobador.html", {'mensaje':mensaje})

    if request.method == 'POST' and 'distribuidor' in request.POST:
        distribuidor = request.POST.getlist('distribuidor')[0]
        Distribuidor(distribuidor=distribuidor,ldap=User.objects.get(username=request.user)).save()
        mensaje = """<div class="alert alert-success alert-dismissible">
                <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                <h4><i class="icon fa fa-check"></i> Exito!</h4>
                El valor de Distribuidor se acaba de agregar con exito a la base de datos.
              </div>"""
        return render(request, "jerarquia_vista_aprobador.html", {'mensaje':mensaje})

    if request.method == 'POST' and 'status' in request.POST:
        status = request.POST.getlist('status')[0]
        Status(status=status,ldap=User.objects.get(username=request.user)).save()
        mensaje = """<div class="alert alert-success alert-dismissible">
                <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                <h4><i class="icon fa fa-check"></i> Exito!</h4>
                El valor de Status se acaba de agregar con exito a la base de datos.
              </div>"""
        return render(request, "jerarquia_vista_aprobador.html", {'mensaje':mensaje})

    if request.method == 'POST' and 'agregar_agente' in request.POST:
        if 'enero' in request.POST:
            enero = True
        else:
            enero = False
        if 'febrero' in request.POST:
            febrero = True
        else:
            febrero = False
        if 'marzo' in request.POST:
            marzo = True
        else:
            marzo = False
        if 'abril' in request.POST:
            abril = True
        else:
            abril = False
        if 'mayo' in request.POST:
            mayo = True
        else:
            mayo = False
        if 'junio' in request.POST:
            junio = True
        else:
            junio = False
        if 'julio' in request.POST:
            julio = True
        else:
            julio = False
        if 'agosto' in request.POST:
            agosto = True
        else:
            agosto = False
        if 'septiembre' in request.POST:
            septiembre = True
        else:
            septiembre = False
        if 'octubre' in request.POST:
            octubre = True
        else:
            octubre = False
        if 'noviembre' in request.POST:
            noviembre = True
        else:
            noviembre = False
        if 'diciembre' in request.POST:
            diciembre = True
        else:
            diciembre = False
        form = agregar_tienda(request.POST)
        if form.is_valid():
            Temporal(a000sap=request.POST.get("a000sap"),
                 codigo_unico=request.POST.get("codigo_unico"),
                 visitas=request.POST.get("visitas"),
                 enero=enero,
                 febrero=febrero,
                 marzo=marzo,
                 abril=abril,
                 mayo=mayo,
                 junio=junio,
                 julio=julio,
                 agosto=agosto,
                 septiembre=septiembre,
                 octubre=octubre,
                 noviembre=noviembre,
                 diciembre=diciembre,
                 latitud=request.POST.get("latitud"),
                 longitud=request.POST.get("longitud"),
                 direccion_fisica=request.POST.get("direccion_fisica"),
                 direccion_fiscal=request.POST.get("direccion_fiscal"),
                 persona_contacto=request.POST.get("persona_contacto"),
                 correo_tienda=request.POST.get("correo_tienda"),
                 correo_empresario=request.POST.get("correo_empresario"),
                 telefono_tienda=request.POST.get("telefono_tienda"),
                 telefono_empresario=request.POST.get("telefono_empresario"),
                 hora_apertura=request.POST.get("hora_apertura"),
                 hora_cierre=request.POST.get("hora_cierre"),
                 empleados=request.POST.get("empleados"),
                 caso_remedy=request.POST.get("caso_remedy"),
                 estado_key=form.cleaned_data["estado_key"],
                 municipio_key=form.cleaned_data["municipio_key"],
                 tipo_key=form.cleaned_data["tipo_key"],
                 tipo_aa_key=form.cleaned_data["tipo_aa_key"],
                 oficina_key=form.cleaned_data["oficina_key"],
                 codigo_deudor_key=form.cleaned_data["codigo_deudor_key"],
                 nombre_key=form.cleaned_data["nombre_key"],
                 direccion_key=form.cleaned_data["direccion_key"],
                 region_key=form.cleaned_data["region_key"],
                 coordinador_key=form.cleaned_data["coordinador_key"],
                 lider_key=form.cleaned_data["lider_key"],
                 gerente_key=form.cleaned_data["gerente_key"],
                 centro_recarga_key=form.cleaned_data["centro_recarga_key"],
                 distribuidor_key=form.cleaned_data["distribuidor_key"],
                 status_key=form.cleaned_data["status_key"],
                 rif_key=form.cleaned_data["rif_key"],
                 punto_rojo=form.cleaned_data["punto_rojo"],
                 ldap=User.objects.get(username=request.user)).save()
            mensaje = """<div class="alert alert-success alert-dismissible">
                <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                <h4><i class="icon fa fa-check"></i> Exito!</h4>
                Nueva tienda o agente  se acaba de agregar con exito a la base de datos.
              </div>"""
        else:
            mensaje = """<div class="alert alert-success alert-dismissible">
                      <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                      <h4><i class="icon fa fa-check"></i> Exito!</h4>
                      Hubo un error en el formulario que no identificamos intenta de nuevo.
                    </div>"""
        return render(request, "jerarquia_vista_aprobador.html", {'mensaje':mensaje})
    return render(request, "jerarquia_vista_aprobador.html", {'f':formularios,'mensaje':mensaje})

def nuevo_agente(request):
    form = agregar_tienda()
    agregar = '<input type="submit" value="Agregar" class="btn btn-block btn-primary" name="agregar_agente">'
    return render(request, "jerarquia_editar.html",{'form':form,'agregar':agregar})
