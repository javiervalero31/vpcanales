from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views
from log.forms import LoginForm  # Importando Formulario de Login

# Estas URL son para loguear, luego se pasa a las url de la app log
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('log.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^login/$', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/login'}),
]
