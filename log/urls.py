from django.conf.urls import url, include
from . import views



urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^mail_informativo/$',views.mail_informativo, name = 'mail_informativo'),
    url(r'^index_update/$',views.index_update, name = 'index_update'),
    url(r'', include('backoffice.urls')),
    url(r'', include('reporteria.urls')),
    url(r'', include('jerarquia.urls')),
    url(r'^recargas/', include('recargas.urls'))
]
