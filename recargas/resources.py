from import_export import resources
from .models import Venta


class VentaResource(resources.ModelResource):
    class Meta:
        model = Venta
