import json
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.db.models import Sum, Count, F, Case, When
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.core import serializers as serial

from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from url_filter.integrations.drf import DjangoFilterBackend

from . import serializers
from .models import Venta
from .filters import VentaFilterSet
from .summaries import VentaTotalOverview

from recargas.serializers import VentaSerializer
from .models import Gerente, Venta, Empresa, Distribuidor, Tiempo, ControlP2P
from recargas.load_recargas import p2p_etl
from sqlalchemy import create_engine
import pandas as ps
from datetime import datetime
# from xml.etree import ElementTree as et
from django.db import connection


class CallPagination(PageNumberPagination):
    page_size = 50


class APIVentaTotalView(APIView):
    """Powers recargas app dashboard."""
    def get(self, request, format=None):
        overview = VentaTotalOverview(filters=request.GET)
        return Response(overview.to_dict())


class VentaList(generics.ListCreateAPIView):
    """Default graph data"""
    start_date = '2017-09-01'
    end_date = '2017-09-30'
    queryset = Venta.objects \
        .filter(tiempo__fecha__range=(start_date, end_date)) \
        .values('tiempo__fecha') \
        .annotate(
            Sum('monto'), Sum('cuota'),
            cumplimiento=Case(
                When(cuota__sum=0, then=0),
                default=Sum('monto') / Sum('cuota') * 100)
        ).order_by('tiempo__fecha')
    serializer_class = VentaSerializer


# Necesita arreglos falta filtrar por distribuidor
class VentaDistribuidor(generics.ListAPIView):
    """Venta por distribuidor ordenada por fecha"""
    serializer_class = VentaSerializer

    def get_queryset(self):
        start_date = datetime.strptime(self.kwargs['d_start'], '%d-%m-%Y')
        end_date = datetime.strptime(self.kwargs['d_end'], '%d-%m-%Y')
        print(start_date)
        print(end_date)
        return Venta.objects \
            .filter(tiempo__fecha__range=(start_date, end_date)) \
            .values('tiempo__fecha') \
            .annotate(Sum('monto'), Sum('cuota')) \
            .order_by('tiempo__fecha')


class IndexView(generic.ListView):
    template_name = 'recargas/index.html'
    context_object_name = 'ventas'

    def get_queryset(self):
        """Retorna todos los gerentes"""
        return Venta.objects.values('tiempo__fecha').exclude(monto__exact=0) \
                            .order_by('-tiempo__fecha')[0]


class MainView(generic.TemplateView):
    template_name = 'recargas/main.html'


def switch_filters(request):
    # filtros = ControlP2P.objects.all()
    filtros = Venta.objects.values('tiempo__fecha').exclude(monto__exact=0) \
                           .order_by('-tiempo__fecha')[0]
    filtros = str(filtros)
    print(filtros)
    data = serial.serialize("json", filtros)
    return JsonResponse(json.loads(data))


def boot_date(request):
    date = Venta.objects.values('tiempo__fecha').exclude(monto__exact=0) \
                        .order_by('-tiempo__fecha')[0]
    data = serial.serialize("json", date)
    return HttpResponse(data, content_type='application/json')


def get_data(request, *args, **kwargs):
    """Dummy function, just for testing porpouse."""
    data = {"ventas": 100000, "cuota": 120000}
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT recargas_gerente.nombre,
            SUM(recargas_venta.monto) as monto_total
            FROM recargas_venta
            INNER JOIN recargas_gerente
            ON recargas_venta.gerente_id = recargas_gerente.id
            INNER JOIN recargas_tiempo
            ON recargas_tiempo.id = recargas_venta.tiempo_id
            WHERE (recargas_tiempo.fecha BETWEEN '2017-10-01' AND '2017-10-31')
            GROUP BY recargas_gerente.nombre
            ORDER BY monto_total DESC;
        """)
        rows = cursor.fetchall()
    return JsonResponse(dict(rows))


class UploadFileForm(forms.Form):
    file = forms.FileField()


def simple_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        load = p2p_etl(request.FILES.get('myfile'))
        if not load:
            return render(request, 'import.html', {
                        'form': form,
                        'title': 'Importe datos de excel en la base de datos',
                        'header': 'Por favor cargue el Insumo correcto:'
            })
        else:
            return render(request, 'import.html', {
                'form': form,
                'header': 'Se cargó ' + str(request.FILES.get('myfile')) +
                ' satisfactoriamente.'
            })
    else:
        form = UploadFileForm()
        print('Formulario desplegado')
    return render(request, 'import.html', {
        'form': form,
        'title': 'Importe datos de excel en la base de datos',
        'header': 'Por favor cargue el Insumo con formato .xls o .xlsx:'
    })


def logout_view(request):
    logout(request)
    render(request, 'index')


@csrf_exempt
def tabla(request):
    ps.set_option('precision', 0)
    columnas = ['Estado']
    engine = create_engine(
                'postgresql://postgres:alphabeta@10.160.9.103:5432/backoffice'
             )
    t = 'escaladas'
    sqltable = ps.read_sql_table(t, engine, columns=columnas)
    # Clean database headers
    sqltable.columns = sqltable.columns.str.replace(' ', '_')
    sqltable.columns = sqltable.columns.str.replace('*', '')
    sqltable.columns = sqltable.columns.str.replace('+', '')
    sqltable.columns = sqltable.columns.str.replace('?', '')
    sqltable.columns = sqltable.columns.str.replace('-', '')
    sqltable.columns = sqltable.columns.str.replace('/', '_')
    sqltable.columns = sqltable.columns.str.replace('.', '')

    table = sqltable.to_json()
    print(type(table))
    return render(request, 'subestados.html', {'tabla': table})
