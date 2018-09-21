from rest_framework import serializers
from reporteria.models import *
from django.db.models.fields import DateField

class ActivacionSerializer(serializers.ModelSerializer):
    fecha = serializers.DateField()
    # cuota = serializers.FloatField()
    class Meta:
        model = Activacion
        fields = ['fecha','cantidad']

class CuotaSerializer(serializers.ModelSerializer):
    fecha = serializers.DateField()
    cuota = serializers.FloatField()
    class Meta:
        model = Cuota
        fields = ['fecha','cuota']

class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = ['nombre_local','codigo']

class GerenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gerente
        fields = ['nombre_gte']

class LiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor
        fields = ['nombre_super']

class CanalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = ['canal']

class TecnologiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activacion
        fields = ['tecnologia']
