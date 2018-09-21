from collections import OrderedDict

from rest_framework import serializers
from rest_framework.fields import SkipField, CharField
from djmoney.contrib.django_rest_framework import MoneyField

from recargas.models import Venta, Direccion, Region, Gerente, Lider, \
                            Empresa, Distribuidor, Tiempo, ControlP2P


class NonNullSerializer(serializers.ModelSerializer):
    """
    This overrides the ModelSerializer to skip keys with null values.
    http://stackoverflow.com/a/28870066/373402
    """

    def to_representation(self, instance):
        """Object instance -> Dict of primitive datatypes."""
        ret = OrderedDict()
        fields = [field for field in self.fields.values() if
                  not field.write_only]

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            if attribute is not None:
                represenation = field.to_representation(attribute)
                if represenation is None:
                    # Do not seralize empty objects
                    continue
                if isinstance(represenation, list) and not represenation:
                    # Do not serialize empty lists
                    continue
                ret[field.field_name] = represenation
        
        return ret


class VentaSerializer(serializers.ModelSerializer):
    """docstring for VentaSerializer."""
    class Meta:
        model = Venta
        fields = ('id','fecha','monto','monto_iva','cuota','tiempo__fecha','monto__sum','cuota__sum', 'cumplimiento')


class VentasSerializer(serializers.ModelSerializer):
    """docstring for VentaSerializer."""
    
    class Meta:
        model = Venta
        # fields = ('id','fecha','monto','monto_iva','cuota','tiempo__fecha','monto__sum','cuota__sum', 'cumplimiento')
        # fields = ('id','fecha','monto','monto_iva','cuota','tiempo__fecha','monto__sum','cuota__sum')
        fields = '__all__'
        # fields = ('id','fecha','monto','monto_iva','cuota','distribuidor','empresa', 'jar') # formting with array


class TiempoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tiempo
        fields = '__all__'


class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
        

class GerenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gerente
        fields = '__all__'

class LiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lider
        fields = '__all__'

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'


class DistribuidorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distribuidor
        fields = '__all__'


class ControlP2PSerialezer(serializers.ModelSerializer):
    class Meta:
        model = ControlP2P
        fields = '__all__'