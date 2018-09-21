from django.contrib import admin
from .models import Direccion, Region, Gerente, Lider, \
     Empresa, Distribuidor, Venta, Tiempo, ControlP2P
# from import_export.admin import ImportExportModelAdmin
# from import_export import resources

admin.site.site_header = "Administración de VP Canales"
admin.site.site_title = "Administración de VP Canales"

# Register your models here.
admin.site.register(Direccion)
admin.site.register(Gerente)
admin.site.register(Lider)
admin.site.register(Region)
admin.site.register(Empresa)
admin.site.register(Distribuidor)
admin.site.register(Venta)
admin.site.register(Tiempo)
admin.site.register(ControlP2P)


# @admin.register(Canal)
# class CanalAdmin(ImportExportModelAdmin):
#     pass


# @admin.register(Direccion)
# class DireccionAdmin(ImportExportModelAdmin):
#     pass


# @admin.register(Gerente)
# class GerenteAdmin(ImportExportModelAdmin):
#     pass


# @admin.register(Region)
# class RegionAdmin(ImportExportModelAdmin):
#     pass


# @admin.register(Empresa)
# class EmpresaAdmin(ImportExportModelAdmin):
#     pass


# @admin.register(Distribuidor)
# class DistribuidorAdmin(ImportExportModelAdmin):
#     pass


# class VentaResource(resources.ModelResource):

#     class Meta:
#         model = Venta


# @admin.register(Venta)
# class VentaAdmin(ImportExportModelAdmin):
#     resource_class = VentaResource


# @admin.register(Jerarquia)
# class JerarquiaAdmin(ImportExportModelAdmin):
#     pass
