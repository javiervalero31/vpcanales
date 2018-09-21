"""Models Based on OLAP theory, arch: star , fact: Venta"""

from django.db import models
from djmoney.models.fields import MoneyField
from datetime import datetime


class ControlP2P(models.Model):
    """Control some interfaces in P2P"""
    nombre = models.CharField(max_length=30, default='Lideres')
    filtro = models.BooleanField(default=True)

    def __str__(self):
        return 'filtro {name} status: '.format(name=self.nombre) + \
         ('Activo' if self.filtro else 'Inactivo')

    class Meta:
        verbose_name_plural = "Control P2P"


# Dimensions:
class Tiempo(models.Model):
    """docstring Canal."""
    def __str__(self):
        return str(self.fecha)
    fecha = models.DateField('', default=datetime.now, unique=True)
    # porcentaje_diario = models.FloatField(default=0.00)

    class Meta:
        verbose_name_plural = "Tiempo"


class Direccion(models.Model):
    """Direccion de las recargas"""
    nombre = models.CharField(max_length=30)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Direcciones"


class Region(models.Model):
    """docstring Region."""
    def __str__(self):
        return self.nombre
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Regiones"


class Gerente(models.Model):
    """docstring Gerente."""
    def __str__(self):
        return '{name} status: '.format(name=self.nombre) + \
         'activo' if self.activo else 'inactivo'
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)


class Lider(models.Model):
    """Lideres"""
    def __str__(self):
        return '{name} status: '.format(name=self.nombre) + \
         'activo' if self.activo else 'inactivo'
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Lideres"


class Empresa(models.Model):
    """docstring Empresa."""
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return '{name} status: '.format(name=self.nombre) + \
         'activo' if self.activo else 'inactivo'


class Distribuidor(models.Model):
    """docstring Distribuidor."""
    def __str__(self):
        return self.vd_code + ' ' + self.zona + ' ' \
            + 'activo' if self.activo else self.vd_code + ' desjerarquizado'
    vd_code = models.CharField(max_length=5, unique=True)
    activo = models.BooleanField(default=True)
    zona = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Distribuidores"


# Fact
class Venta(models.Model):
    """Venta P2P"""
    monto = MoneyField(max_digits=12, decimal_places=2, default_currency='VEF')
    monto_iva = MoneyField(max_digits=12, decimal_places=2, default_currency='VEF')
    cuota = MoneyField(max_digits=12, decimal_places=2, default_currency='VEF')
    tiempo = models.ForeignKey(Tiempo, on_delete=models.CASCADE, default=1)
    distribuidor = models.ForeignKey(Distribuidor, on_delete=models.CASCADE, default=1)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, default=1)
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE, default=1)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, default=1)
    gerente = models.ForeignKey(Gerente, on_delete=models.CASCADE, default=1)
    lider = models.ForeignKey(Lider, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.distribuidor.vd_code + ': ' + self.empresa.nombre + ' \
    ' + self.distribuidor.zona + ' al ' + str(self.tiempo.fecha)

    def fecha(self):
        return self.tiempo.fecha

    def tiempo__fecha(self):
        return self.tiempo.fecha

    def monto__sum(self):
        pass

    def cuota__sum(self):
        pass

    def cumplimiento(self):
        return (self.monto / self.cuota) * 100 if self.cuota != 0 else 0

    def jar(self):
        return [self.gerente.nombre, self.region.nombre]
