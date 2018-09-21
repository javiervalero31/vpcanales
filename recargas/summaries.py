from collections import Counter
from datetime import timedelta
from decimal import *

from django.db.models import Min, Max, Count, Case, When, IntegerField, FloatField, DecimalField, F, \
    Avg, DurationField, Q, Sum, Func, CharField, Value as V
from django.db.models.functions import ExtractMonth, ExtractYear, Cast, Concat
from url_filter.filtersets import StrictMode


from .django_future_expressions import Window,  ExpressionList
from .filters import VentaFilterSet
from .models import Venta, Gerente, Lider, Empresa, Distribuidor, Direccion

def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


class VentaOverview:

    def __init__(self, filters):
        self._filters = filters
        self.filter = VentaFilterSet(data= filters,
                                     queryset=Venta.objects.filter(),
                                     strict_mode=StrictMode.fail)

        self.bounds = self.qs.aggregate(min_time=Min('tiempo__fecha'), 
                                        max_time=Max('tiempo__fecha'))
        if self.bounds['max_time'] and self.bounds['min_time']:
             self.span = self.bounds['max_time'] - self.bounds['min_time']
        else:
            self.span = timedelta(0, 0)

    @property
    def qs(self):
        return self.filter.filter()

    def count(self):
        return self.qs.count()

    def precision(self):
        if self.span >= timedelta(days=31):
            return 'month'
        elif self.span >= timedelta(days=7):
            return 'day'

    def merge_data(self, src_data, all_ids):
        src_data = list(src_data)
        all_ids = set(all_ids)
        present_ids = set(x['id'] for x in src_data)

        if len(present_ids) > 0:
            for id in all_ids.difference(present_ids):
                src_data.append(merge_dicts({"id": id}, self.default))

        return src_data

    def direccion_ids(self):
        return dict(Direccion.objects.all().values_list('nombre','id'))

    def region_ids(self):
        return dict(Region.objects.all().values_list('nombre','id'))

    def gerente_ids(self):
        return dict(Gerente.objects.all().values_list('nombre','id'))

    def empresa_ids(self):
        return dict(Empresa.objects.all().values_list('nombre', 'id'))

    def distribuidor_ids(self):
        return dict(Distribuidor.objects.all().values_list('nombre','id'))

    def by_dow(self):
        results = self.qs \
            .annotate(id_=F('tiempo__fecha'), name=F('tiempo__fecha')) \
            .values("id") \
            .annotate(**self.annotations)

        return self.merge_data(results, range(0, 7))

    def by_direccion(self):
        all_in_field = Direccion.objects.annotate(
            address=F("nombre"),
            key=F("id")).values('id', 'nombre', 'activo').order_by('nombre')
        return all_in_field

    def by_empresa(self):
        all_in_field = Empresa.objects.annotate(
            empresa=F("nombre"),
            key=F("id")).values('id', 'nombre', 'activo').order_by("nombre")
        return all_in_field

    def by_gerente(self):
        all_in_field = Gerente.objects.annotate(
            manager=F("nombre"),
            key=F("id")).values('id', 'nombre', 'activo').order_by("nombre")
        return all_in_field

    def by_lider(self):
        all_in_field = Lider.objects.annotate(
            manager=F("nombre"),
            key=F("id")).values('id', 'nombre', 'activo').order_by("nombre")
        return all_in_field
        # results = self.qs \
        #     .annotate(ids=F("gerente_id"),
        #               name=F("gerente__nombre")) \
        #     .values("name", "id") \
        #     .annotate(**self.annotations)
        
        # results = list(results)
        # present_ids = set(x['id'] for x in results)

        # if len(present_ids) > 0:
        #     for row in all_in_field:
        #         if row['id'] not in present_ids:
        #             row.update(**self.default)
        #             results.append(row)

        # return results

    def by_distribuidores(self):
        all_in_field = Distribuidor.objects.annotate(
            zone=F("zona"),
            key=F("id")).values('id','vd_code', 'zona', 'activo').order_by('zona')
        
        return all_in_field
        # results = self.qs \
        #     .annotate(key=F('id')), \
        #         empresa =F('nombre') \
        #     .values('id', 'nombre') \
        #     .annotate(**self.annotations)

        # results = list(results)

        # present_ids = set(x['id'] for x in results)

        # if len(present_ids) > 0:
        #     for row in all_in_field:
        #         if row['id'] not in present_ids:
        #             row.update(**self.default)
        #             results.append(row)
        
        # return results


class Round(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 1)'


class RoundDecimal(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s,0)'

class LagLeadFunction(Func):
    window_compatible = True

    def __init__(self, expression, offset=1, default=None, **extra):
        if expression is None:
            raise ValueError(
                '%s requires a non-null source expression.' %
                self.__class__.__name__
            )
        if offset is None or offset <= 0:
            raise ValueError(
                '%s requires a positive integer for the offset.' %
                self.__class__.__name__
            )
        args = (expression, offset)
        if default is not None:
            args += (default,)
        super().__init__(*args, **extra)

    def _resolve_output_field(self):
        sources = self.get_source_expressions()
        return sources[0].output_field

class Lag(LagLeadFunction):
    function = 'LAG'
    name = 'Lag'


class Lead(LagLeadFunction):
    function = 'LEAD'
    name = 'Lead'

class VentaTotalOverview(VentaOverview):
    annotations = dict(total=Count("id"))
    default = dict(total=0)

    def real_up_to(self):
        return Venta.objects.values('tiempo__fecha').exclude(monto__exact=0).order_by('-tiempo__fecha')[0]

    def total_by_month(self):
        results = self.qs \
         .aggregate(total_venta=RoundDecimal(Sum('monto')), total_cuota=RoundDecimal(Sum('cuota')), \
            cumplimiento= Case(When(total_cuota= 0, then=0), default=Round(Sum('monto') / Sum('cuota') * 100))
        )
           
        return results

    def total_fixed_months(self):
        return Venta.objects.values(
                                    month=ExtractMonth('tiempo__fecha'),
                                    year=ExtractYear('tiempo__fecha')
                                    ) \
                        .annotate(
                            total_monto=Sum('monto'),
                            total_cuota=Sum('cuota'),
                            # intermensual = Lag(
                            #     Sum(
                            #         F('monto'), 
                            #         output_field=DecimalField(decimal_places=3, max_digits=10,)
                            #     )
                            # )
                        ) \
                        .order_by('-month') ## fixed
        # return Venta.objects.aggregate(intermensual = Lag(Sum('monto'))) 

    def total_by_months(self):
        result = self.qs.values(
                        month=ExtractMonth('tiempo__fecha'),
                        year=ExtractYear('tiempo__fecha') 
                    ) \
                    .annotate(total=Sum('monto'), cuota_total=Sum('cuota')).order_by('month') \
                    .order_by('-month')
        # print(result.query)
        return result        

    def total_by_date(self):
        results = self.qs \
            .values("tiempo__fecha") \
            .annotate(
                    #   direcciones=F('direccion__nombre'), 
                    #   gerente=F('gerente__nombre'),
                    #   region=F('region__nombre'),
                    #   distribuidor_agrupado=F('empresa__nombre'),
                    #   codigo_vd=F('distribuidor__vd_code'),
                    #   distribuidor_por_zona=F('distribuidor__zona'),
                      monto_total=RoundDecimal(Sum('monto')),
                      cuota_total=RoundDecimal(Sum('cuota')),
                      porcentaje_cumplimiento= Case(
                          When(cuota_total = 0, then=0), default=Round(Sum('monto') / Sum('cuota') * 100) ),
            ) \
            .order_by("tiempo__fecha") 
       
        return results

    def por_direccion(self):
        return self.qs.values("direccion__nombre").distinct().order_by("direccion__nombre")

    def por_gerente(self):
        return self.qs.values("gerente__nombre").distinct().order_by("gerente__nombre")

    def por_lider(self):
        return self.qs.values("lider__nombre").distinct().order_by("lider__nombre")

    def por_empresa(self):
        return self.qs.values("empresa__nombre").distinct().order_by("empresa__nombre")
    
    def por_distribuidor(self):
        return self.qs.values("distribuidor__zona").distinct()

    def gerente_by_direccion(self):
        return self.qs.values("direccion__nombre").annotate( manager=F('gerente__nombre')) \
        .distinct().order_by('gerente__nombre')

    def empresa_by_gerente(self):
        return self.qs.values("gerente").annotate( nombre=F('empresa__nombre')).distinct().order_by('empresa__nombre')

    def distribuidor_by_direccion(self):
        return self.qs.values("direccion")\
            .annotate( nombre=F('distribuidor__zona')) \
            .distinct()
    
    def distribuidor_by_empresa(self):
        return self.qs.values('empresa__nombre').annotate( zona=F('distribuidor__zona')).distinct()

    def part_by_manager(self):
        results = self.qs \
            .values('gerente__nombre') \
            .annotate(monto_total=RoundDecimal(Sum('monto')),\
                      cuota_total=RoundDecimal(Sum('cuota')), 
                      cumplimiento= Case(
                                    When (cuota_total = 0, then=0),\
                                          default=Round(Sum('monto') / Sum('cuota') * 100 ))
                     ) \
            .order_by('-cumplimiento')
            
        # print(self.qs.query)
        # print(self.qs)
        # print(results.query)
        return results
    def part_by_leader(self):
        results = self.qs \
            .values('lider__nombre') \
            .annotate(monto_total=RoundDecimal(Sum('monto')),\
                      cuota_total=RoundDecimal(Sum('cuota')), 
                      cumplimiento= Case(
                          When (cuota_total = 0, then=0),\
                                 default=Round(Sum('monto') / Sum('cuota') * 100 ))
                                 ) \
            .order_by('-cumplimiento')
        return results

    def part_by_direction(self):
        """Participation by Direction"""
        results = self.qs \
            .values('direccion__nombre') \
            .annotate(monto_total=RoundDecimal(Sum('monto')),\
                      cuota_total=RoundDecimal(Sum('cuota')),
                      cumplimiento = Case(
                          When (cuota_total = 0, then=0),\
                                default=Round(Sum('monto') / Sum('cuota') * 100 )),
                    #   pos=Window(
                    #       expression=Lag(
                    #            Sum(
                    #                 F('monto'), 
                    #             )
                    #       ),
                    #       output_field=DecimalField(decimal_places=3, max_digits=10,),
                        #   partition_by=[F('monto'), F('cuota')],
                    #       order_by=F('monto')           
                    #   )
                      ) \
            .order_by('-cumplimiento')
            # .extra('pos': "ROW_NUMBER() OVER(ORDER BY  )")
        
        return results     

    def part_by_region(self):
        """Participation by Region"""
        results = self.qs \
            .values('region__nombre') \
            .annotate(monto_total=RoundDecimal(Sum('monto')),\
                      cuota_total=RoundDecimal(Sum('cuota')),
                      cumplimiento = Case(
                          When (cuota_total = 0, then=0),\
                                default=Round(Sum('monto') / Sum('cuota') * 100 ))
                      ) \
            .order_by('-cumplimiento')
        return results     


    def part_by_dist(self):
        """Participation by Distribuitor"""
        results = self.qs \
            .values('distribuidor__zona') \
            .annotate(monto_total=RoundDecimal(Sum('monto')),\
                      cuota_total=RoundDecimal(Sum('cuota')),
                      cumplimiento= Case(
                          When (cuota_total = 0, then=0),\
                                default=Round(Sum('monto') / Sum('cuota') * 100 ))
                      ) \
            .order_by('-cumplimiento')
        return results

    def part_by_company(self):
        """Participation by Company"""
        results = self.qs \
            .values('empresa__nombre') \
            .annotate(monto_total=RoundDecimal(Sum('monto')),\
                      cuota_total=RoundDecimal(Sum('cuota')),
                      cumplimiento = Case(
                          When (cuota_total = 0, then=0),\
                                default=Round(Sum('monto') / Sum('cuota') * 100 ))
                      ) \
            .order_by('-cumplimiento')
        return results

    def probable_cierre(self):
        """Returns problade de cierre."""
        getcontext().prec = 7
        results = self.qs \
        .aggregate(total_venta=Sum('monto'), total_cuota=Sum('cuota'), \
            cumplimiento= Case(
                          When(total_cuota= 0, then=0), default=Sum('monto') / Sum('cuota')),
             )
        try:
            # print(self._filters)
            if 'tiempo__fecha__lte' in self._filters:
                qdict = self._filters.copy()
                qdict.pop('tiempo__fecha__lte')
                qdict.pop('tiempo__fecha__gte')
                print(qdict)

                month_fee = Venta.objects.filter(**qdict.dict()) \
                                    .values(
                                        month=ExtractMonth('tiempo__fecha'),
                                        year=ExtractYear('tiempo__fecha')
                                    ) \
                                    .annotate(
                                        cuota_mes=Sum('cuota'),
                                    ) \
                                    .order_by('-year','-month')[0]
                
                if not None in results.values():
                    pc_values = {**results,  **dict(month_fee)}
                    cf = pc_values['cuota_mes'] - pc_values['total_cuota']
                    # print('Venta Acumulada: ', pc_values['total_venta'])
                    # print('Cuota Faltante: ', cf)
                    # print('Diferencial Cuota: ', cf * abs(Decimal(pc_values['cumplimiento'] - 100) / Decimal(100) ))
                    # print('cumplimiento: ', pc_values['cumplimiento'])
                    # print(pc_values)
                    # print(pc_values['total_venta'] + cf + cf * (pc_values['cumplimiento'] - 1) ) 
                    pc = dict({'pc': pc_values['total_venta'] + cf + cf * (pc_values['cumplimiento'] - 1 )})
                    pc_values = { **pc, **results,  **dict(month_fee)} 
                    return  pc_values
                else:
                    return results

        except IndexError:
            print('Index fuera de rango')
            return results
        
        return results


    def to_dict(self):
        return { 
        'filter': self.filter.data,
        'bounds': self.bounds,
        'count': self.count(),
        'precision': self.precision(),
        'real_up_to': self.real_up_to(),
        'totales': self.total_by_month(),
        'probable_cierre': self.probable_cierre(),
        'mensuales': self.total_by_months(),
        'mensuales_fijos': self.total_fixed_months(),
        'part_direction': self.part_by_direction(),
        'part_region': self.part_by_region(),
        'part_company': self.part_by_company(),
        'part_distribuitor': self.part_by_dist(),
        'total_gerentes': self.part_by_manager(),
        'part_leader': self.part_by_leader(),
        'por_direccion': self.por_direccion(),
        'por_gerente': self.por_gerente(),
        'por_lider': self.por_lider(),
        'por_empresa': self.por_empresa(),
        'por_distribuidor': self.por_distribuidor(),
        'empresa_por_gerente': self.empresa_by_gerente(),
        'distribuidor_por_direccion': self.distribuidor_by_direccion(),
        'distribuidor_por_empresa': self.distribuidor_by_empresa(),
        'gerentes_por_direccion': self.gerente_by_direccion(),
        'ventas_por_fecha': self.total_by_date(),
        'direcciones': self.by_direccion(),
        'gerentes': self.by_gerente(),
        'lideres': self.by_lider(),
        'distribuidores_agrupados': self.by_empresa(),
        'distribuidores': self.by_distribuidores(),
    }