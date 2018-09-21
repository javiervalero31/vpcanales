from rest_framework import viewsets
from url_filter.integrations.drf import DjangoFilterBackend
from .models import Direccion, Region, Gerente, Empresa, Distribuidor, Tiempo,\
                    Venta, Lider, ControlP2P
from .serializers import DireccionSerializer, RegionSerializer, \
                         GerenteSerializer, EmpresaSerializer, \
                         DistribuidorSerializer, VentaSerializer, \
                         TiempoSerializer, VentasSerializer, \
                         LiderSerializer, ControlP2PSerialezer


class VentasViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentasSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'tiempo', 'direccion', 'empresa', ]


class DireccionViewSet(viewsets.ModelViewSet):
    queryset = Direccion.objects.all()
    serializer_class = DireccionSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'nombre', 'activo']


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'nombre', 'activo']


class GerenteViewSet(viewsets.ModelViewSet):
    queryset = Gerente.objects.all()
    serializer_class = GerenteSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'nombre', 'activo']


class LiderViewSet(viewsets.ModelViewSet):
    queryset = Lider.objects.all()
    serializer_class = LiderSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'nombre', 'activo']


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'nombre', 'activo']


class DistribuidorViewSet(viewsets.ModelViewSet):
    queryset = Distribuidor.objects.all()
    serializer_class = DistribuidorSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'zona', 'activo', 'vd_code']


class TiempoViewSet(viewsets.ModelViewSet):
    queryset = Tiempo.objects.all()
    serializer_class = TiempoSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'fecha']


class ControlP2PViewSet(viewsets.ModelViewSet):
    queryset = ControlP2P.objects.all()
    serializer_class = ControlP2PSerialezer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'filtro_lideres']
