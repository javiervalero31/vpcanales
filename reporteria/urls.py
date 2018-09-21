from django.conf.urls import url, include
from . import views
#Se importan las funciones y se le asigna un alias
import reporteria.views as reporteria
import reporteria.validador as val
from rest_framework import routers
from reporteria import viewsets


router = routers.DefaultRouter()
# router.register(r'cuota-activacion', viewsets.ActivacionCuotaAPIView)

urlpatterns = [
	url(r'^reporte/$',reporteria.reporte, name= 'reporte'),
	url(r'^carga_data/$',val.validator, name = 'carga_data'),
	url(r'^comercial_grafica/$',views.comercial_grafica),
	url(r'^prueba2/$',views.abrirModal),
	url(r'api-reporteria/', include(router.urls)),
	url(r'api-reporteria/cuota/', viewsets.ActivacionCuotaAPIView.as_view()),
	url(r'^api-reporteria/',include('rest_framework.urls',namespace='rest_framework')),





]
