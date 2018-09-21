from django.conf.urls import url, include
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from . import views

from .viewsets import DireccionViewSet, RegionViewSet, GerenteViewSet, \
    LiderViewSet, EmpresaViewSet, DistribuidorViewSet, VentasViewSet, \
    TiempoViewSet, ControlP2PViewSet

app_name = 'recargas'  # URL namespace

router = routers.DefaultRouter()

router.register(r'ventas', VentasViewSet)
router.register(r'direcciones', DireccionViewSet)
router.register(r'regiones', RegionViewSet)
router.register(r'gerentes', GerenteViewSet)
router.register(r'lideres', LiderViewSet)
router.register(r'empresas', EmpresaViewSet)
router.register(r'distribuidores', DistribuidorViewSet)
router.register(r'tiempo', TiempoViewSet)
router.register(r'filtros', ControlP2PViewSet)

urlpatterns = [
    url(r'^admin/logout$', views.logout_view, name='admin/logout'),
    url(r'^P2P/$', views.IndexView.as_view(), name='index'),  # /recargas/P2P
    url(r'^api/P2P/recargas_resumen/$', views.APIVentaTotalView.as_view()),
    url(r'^api/', include(router.urls)),  # Api Root (router)
    url(r'^import/$', views.simple_upload),
    url(r'^P2P/api/P2P/(?P<d_start>[0-9]{2}-[0-9]{2}-[0-9]{4})-\
    (?P<d_end>[0-9]{2}-[0-9]{2}-[0-9]{4})/$',
        views.VentaDistribuidor.as_view()),
    url(r'^api/P2P/$', views.VentaList.as_view()),
    url(r'^api/data/$', views.get_data, name='api-data'),  # dummy data
    url(r'^subestados$', views.tabla),
    url(r'^main/$', views.MainView.as_view(), name='main'),
    url(r'^switch_filter/$', views.switch_filters),
    url(r'^boot_date_p2p/$', views.boot_date),
    url(r'^.*$', TemplateView.as_view(template_name='recargas/spa.html')),
]

# # Rod: DRF don't allow this line.
# urlpatterns = format_suffix_patterns(urlpatterns)
