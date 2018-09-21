from rest_framework import serializers
from .models import Imei


class ImeiSerializer(serializers.ModelSerializer):

    class Meta:
        model = Imei
        fields = '__all__'
