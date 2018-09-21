from django.conf.urls import url, include
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)
from rest_framework import views, serializers, status
from rest_framework.response import Response
from api.views import ImeiList, upload_imei_data


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class EchoView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

urlpatterns = [
    url(r'^$', get_schema_view()),
    url(r'^upload/$', upload_imei_data),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/token/obtain/$', TokenObtainPairView.as_view()),
    url(r'^auth/token/refresh/$', TokenRefreshView.as_view()),
    url(r'^echo/$', EchoView.as_view()),
    url(r'^imei-v1/$', ImeiList.as_view(), name='api-imei-list'),
]