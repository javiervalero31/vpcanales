from django.conf.urls import url, include
from jerarquia import views



urlpatterns = [
    url(r'^jerarquia/$', views.jerarquia, name='jerarquia'),
    url(r'^editar/(?P<codigo_unico>\w+)/$', views.consulta_codigo, name='consulta'),
    url(r'^aprobar/', views.aprobar, name='aprobar'),
    url(r'^aprobar_cambio/(?P<codigo_unico>\w+)/$', views.consulta_cambio, name='aprobar_cambio'),
    url(r'^cerrar/$', views.cerrar_jerarquia, name='cerrar'),
    url(r'^descarga_especial/$', views.descarga_especial, name='descarga_especial'),
    url(r'^descarga_jerarquia/$', views.descarga_jerarquia, name='descarga_jerarquia'),
    url(r'^formulario_aprobador/$', views.formularios_vista_aprobador, name='vista_aprobador'),
    url(r'^nuevo_agente/$', views.nuevo_agente, name='agregar_agente'),]
