from rest_framework import viewsets
from reporteria.serializer import *
from reporteria.models import *
from url_filter.integrations.drf import DjangoFilterBackend
from django.db.models import Sum, Count, F

import itertools
from drf_multiple_model.views import ObjectMultipleModelAPIView, FlatMultipleModelAPIView

class ActivacionCuotaAPIView(ObjectMultipleModelAPIView):
    def get_querylist(self):
        cuota_params={}
        activacion_params={}
        gerente_params={}
        lider_params={}
        codigo_params={}
        canal_params={}
        tecnologia_params={}
        fecha1 = self.request.query_params['fecha1']
        fecha2 = self.request.query_params['fecha2']

        if 'gerente' in self.request.query_params.keys():
            cuota_params['local_key__jerarquia__gerente_key__nombre_gte']=self.request.query_params['gerente']
            activacion_params['local_key__jerarquia__gerente_key__nombre_gte']=self.request.query_params['gerente']
            lider_params['jerarquia__gerente_key__nombre_gte']=self.request.query_params['gerente']
            codigo_params['jerarquia__gerente_key__nombre_gte']=self.request.query_params['gerente']
            canal_params['jerarquia__gerente_key__nombre_gte']=self.request.query_params['gerente']

        if 'lider' in self.request.query_params.keys():
            cuota_params['local_key__jerarquia__supervisor_key__nombre_super']=self.request.query_params['lider']
            activacion_params['local_key__jerarquia__supervisor_key__nombre_super']=self.request.query_params['lider']
            gerente_params['jerarquia__supervisor_key__nombre_super']=self.request.query_params['lider']
            codigo_params['jerarquia__supervisor_key__nombre_super']=self.request.query_params['lider']
            canal_params['jerarquia__supervisor_key__nombre_super']=self.request.query_params['lider']

        if 'canal' in self.request.query_params.keys():
            cuota_params['local_key__canal']=self.request.query_params['canal']
            activacion_params['local_key__canal']=self.request.query_params['canal']
            gerente_params['jerarquia__local__canal']=self.request.query_params['canal']
            lider_params['jerarquia__local__canal']=self.request.query_params['canal']
            codigo_params['canal']=self.request.query_params['canal']

        if 'codigo' in self.request.query_params.keys():
            cuota_params['local_key__codigo']=self.request.query_params['codigo']
            activacion_params['local_key__codigo']=self.request.query_params['codigo']
            gerente_params['jerarquia__local__codigo']=self.request.query_params['codigo']
            lider_params['jerarquia__local__codigo']=self.request.query_params['codigo']
            canal_params['codigo']=self.request.query_params['codigo']

        if 'tecnologia' in self.request.query_params.keys():
            activacion_params['tecnologia']=self.request.query_params['tecnologia']
            cuota_params['local_key__activacion__tecnologia']=self.request.query_params['tecnologia']


        querylist = (
            {'queryset': Cuota.objects.filter(fecha_cuota__range=(fecha1,fecha2),**cuota_params)\
            .values(fecha=F('fecha_cuota')).annotate(cuota=Sum('cuota_activaciones_total')),
             'serializer_class':CuotaSerializer},

            {'queryset': Activacion.objects.filter(fecha_actividad__range=(fecha1,fecha2),**activacion_params)\
            .values(fecha=F('fecha_actividad')).annotate(cantidad=Sum('cantidad')),
             'serializer_class':ActivacionSerializer},

            {'queryset': Supervisor.objects.filter(**lider_params,activo=1)\
            .distinct().order_by('nombre_super'),
             'serializer_class':LiderSerializer},

            {'queryset': Gerente.objects.filter(**gerente_params,activo=1)\
            .values('nombre_gte').distinct().order_by('nombre_gte'),
             'serializer_class':GerenteSerializer},

            {'queryset': Local.objects.filter(**codigo_params,activo=1)\
            .values('codigo','nombre_local').distinct().order_by('codigo'),
             'serializer_class':LocalSerializer},

            {'queryset': Local.objects.filter(**canal_params,activo=1).values('canal')\
            .distinct().order_by('canal'),
             'serializer_class':CanalSerializer, 'label':'canal'},

            {'queryset': Activacion.objects.filter(**tecnologia_params).values('tecnologia')\
             .distinct().order_by('tecnologia'),
             'serializer_class':TecnologiaSerializer, 'label':'tecnologia'}

        )
        return querylist
