from django.conf.urls import url, include
from . import escaladas, resueltas
#Se importan las funciones y se le asigna un alias
import backoffice.resueltas as re
import backoffice.escaladas as es
import backoffice.upload as up
import backoffice.grupor as gr

urlpatterns = [
    url(r'^escaladas/$', es.subtabla, name='escaladas'),
    url(r'^resueltas/$',re.subtabla, name= 'resueltas'),
    url(r'^upload/$', up.upload_file, name='upload')
]
