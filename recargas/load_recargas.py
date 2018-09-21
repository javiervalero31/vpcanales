from django.db import transaction, IntegrityError
from recargas.models import (Direccion, Region, Gerente, Lider, \
                             Distribuidor, Empresa, Venta, Tiempo)
import pandas as pd
import time
import logging as log
from datetime import datetime


def timeit(func_to_decorate):
    """Decorator generator that logs the time it takes a function to execute"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func_to_decorate(*args, **kwargs)
        elapsed = (time.time() - start)
        log.debug("[TIMING]: %s - %s s" % (func_to_decorate.__name__, elapsed))
        print("[TIMING]: %s - %s s" % (func_to_decorate.__name__, round(elapsed, 2)))
        # if 'log_time' in kwargs:
        #     name = kwargs.get('log_name', func_to_decorate.__name__.upper())
        #     kwargs['log_time'][name] = int((elapsed - start) * 1000)
        # else:
        #     print ('%r  %2.2f ms' % \
        #           (func_to_decorate.__name__, (elapsed - start) * 1000))
        return result

    wrapper.__doc__ = func_to_decorate.__doc__
    wrapper.__name__ = func_to_decorate.__name__
    return wrapper


@timeit
def p2p_etl(ruta_insumo):
    # EXTRACT

    # ruta_insumo = 'C:/Users/E09428/Desktop/P2P201710.xlsx'
    xlsx = pd.ExcelFile(ruta_insumo)
    try:
        df = pd.read_excel(xlsx, 'Data P2P')
    except:
        return False
# TRANSFORM

    direcciones = df.loc[:, 'Dirección'].unique()
    regiones = df.loc[:, 'Región'].unique()
    gerentes = df.loc[:, 'Gerente'].unique()
    lideres = df.loc[:, 'Líder'].unique()
    empresas = df.loc[:, 'Distribuidor'].unique()
    distribuidores = df.loc[:, ('Cod VD', 'Sucursal')].drop_duplicates()
    tiempos = df.loc[:, ('Fecha')].drop_duplicates()
    # mes = pd.to_datetime(df.loc[:,'Fecha'].unique())
    # domingos = df.loc[df['% Diario'] == 0 ].loc[:,'Fecha'].unique()
    # domingos.loc[:,'Fecha'].unique()
    # print(distribuidores)
    # print(tiempos)
# LOAD

    @timeit
    def save_name_dim(unique_list, to_model):
        """Save the name/nombre of Model passed from a unique list"""
        to_model.objects.all().update(activo=False)
        for item in unique_list:
            try:
                to_model.objects.get(nombre__iexact=item)
                to_model.objects.filter(nombre__iexact=item).update(activo=True)
                continue
            except to_model.DoesNotExist:
                q = to_model(nombre=item)
                q.save()
                continue

    @timeit
    def save_time_dim(time_df, to_model):
        """Save time dimension"""
        for row in time_df.iteritems():
            try:
                to_model.objects.get(fecha__iexact=row[1])
                continue
            except to_model.DoesNotExist:
                try:
                    to_model(fecha=row[1]).save()
                    continue
                except:
                    transaction.rollback()
                    # print("La fecha", row[1], "ya se ha cargado, deshaciendo.")
            finally:
                # print("Tiempo cargado", row[1])
                pass

    @timeit
    def save_distribuidor_dim(distribuidor_df, to_model):
        to_model.objects.all().update(activo=False)
        for row in distribuidor_df.itertuples():
            try:

                if (row[2] != 'DESJERARQUIZADO'):
                    to_model.objects.get(vd_code__iexact=row[1], zona__iexact=row[2])
                    to_model.objects.filter(vd_code__iexact=row[1], zona__iexact=row[2]).update(activo=True)
                else:
                    to_model.objects.get(vd_code__iexact=row[1], zona__iexact=row[2])
                    to_model.objects.filter(vd_code__iexact=row[1], zona__iexact=row[2]).update(activo=False)

                    # if (col['Distribuidor por Zona'] == 'DESJERARQUIZADO'):
                    #     raise ValueError('Miguel Angel')
                continue
            except to_model.DoesNotExist:
                try:
                    print('El distribuidor ' + row[1] + ' no existe se procedera a cargar.')
                    # print(type(row[1]),type(row[2]) )
                    q = to_model(vd_code=row[1], zona=row[2], activo=False if (row[2] == 'DESJERARQUIZADO') else True)
                    q.save()
                    continue
                except IntegrityError:
                    # raise ValueError('El' + row[1] + ' cambio de nombre')
                    q = to_model.objects.filter(vd_code=row[1]).update(zona=row[2])
                    # raise ValueError('Se sobrescribio un distribuidor.')
                    print("Este distribuidor", row[2], "SE ACTUALIZO!!!")
                except Exception as e:
                    print('La exepcion es: '+ str(e))
                    raise e

                except TypeError:
                    print("Type Error!!!!")
                    continue
                    # q.save()
                    # transaction.rollback()
                    # print("Este distribuidor", row[2], "ya esta cargado")

            finally:
                # print(type(row[1]),type(row[2]) )
                # print("Distribuidor cargado", row[2], row[1])
                pass

    save_name_dim(direcciones, Direccion)
    save_name_dim(regiones, Region)
    save_name_dim(gerentes, Gerente)
    save_name_dim(lideres, Lider)
    save_name_dim(empresas, Empresa)

    save_time_dim(tiempos, Tiempo)

    save_distribuidor_dim(distribuidores, Distribuidor)

    # Delete Facts
    Venta.objects.filter(tiempo__fecha__range=(tiempos.min(), tiempos.max())).delete()

    # Load Facts
    for row in df.itertuples():
        try:
            # print("Guardando venta de", row[2], row[7], "al:", row[1])
            q = Venta(monto = row[-1],
                monto_iva = row[-2],
                cuota = row[-3],
                tiempo = Tiempo.objects.get(fecha=row[1]),
                distribuidor = Distribuidor.objects.get(vd_code__iexact=row[2]),
                empresa = Empresa.objects.get(nombre__iexact=row[7]),
                direccion = Direccion.objects.get(nombre__iexact=row[3]),
                region = Region.objects.get(nombre__iexact=row[4]),
                gerente = Gerente.objects.get(nombre__iexact=row[5]),
                lider= Lider.objects.get(nombre__iexact=row[6]),
            )
            q.save() 
            continue
        except (Tiempo.DoesNotExist, Distribuidor.DoesNotExist, Empresa.DoesNotExist, \
            Direccion.DoesNotExist, Region.DoesNotExist,  Gerente.DoesNotExist):
            try:
                # THIS never should run...
                # Run if not records on the DB # ???
                print("Nuevo Registro, almacenando venta de", row[2], "al:", row[1])
                Venta(
                    monto = row[-1],
                    monto_iva = row[-2],
                    cuota = row[-3],
                    tiempo = Tiempo.objects.get(fecha=row[1]),
                    distribuidor = Distribuidor.objects.get(vd_code__iexact=row[2]),
                    empresa = Empresa.objects.get(nombre__iexact=row[7]),
                    direccion = Direccion.objects.get(nombre__iexact=row[3]),
                    region = Region.objects.get(nombre__iexact=row[4]),
                    gerente = Gerente.objects.get(nombre__iexact=row[5]),
                    lider= Lider.objects.get(nombre__iexact=row[6]),
                ).save()
                continue
            except Exception as e:
                    print(row)
                    print(row[7], '-')
                    print(row.Distribuidor, '===')
                    print('La exepcion es: ' + str(e))
                    raise ValueError(
                        'Un valor no se cargo correctamente. ',
                        'La exepcion es: ' + str(e)
                    )

    ## UPDATE
    # try:
    #     Venta.objects.filter(distribuidor__activo=False) \
    #         .update(direccion=Direccion.objects.get(nombre__iexact='DESJERARQUIZADO'), 
    #                 region=Region.objects.get(nombre__iexact='DESJERARQUIZADO'), 
    #                 gerente=Gerente.objects.get(nombre__iexact='DESJERARQUIZADO'),
    #                 lider=Lider.objects.get(nombre__iexact='DESJERARQUIZADO'),
    #                 empresa=Empresa.objects.get(nombre__iexact='DESJERARQUIZADO'),
    #                 distribuidor=Distribuidor.objects.get(vd_code__iexact='VD00'))
   
    # except (Direccion.DoesNotExist, Region.DoesNotExist, Gerente.DoesNotExist, \
            # Lider.DoesNotExitst, Empresa.DoesNotExist, Distribuidor.DoesNotExist):
            # Direccion(nombre='DESJERARQUIZADO').save()
            # Region(nombre='DESJERARQUIZADO').save()
            # Gerente(nombre='DESJERARQUIZADO').save()
            # Lider(nombre='DESJERARQUIZADO').save()
            # Empresa(nombre='DESJERARQUIZADO').save()
            # Distribuidor(vd_code='VD00', zona='DESJERARQUIZADO').save()
            # print("Creado DESJERARQUIZADO para las dimesiones") 

            # Venta.objects.filter(distribuidor__activo=False) \
            # .update(direccion=Direccion.objects.get(nombre__iexact='DESJERARQUIZADO'), 
            #         region=Region.objects.get(nombre__iexact='DESJERARQUIZADO'), 
            #         gerente=Gerente.objects.get(nombre__iexact='DESJERARQUIZADO'),
            #         lider=Lider.objects.get(nombre__iexact='DESJERARQUIZADO'),
            #         empresa=Empresa.objects.get(nombre__iexact='DESJERARQUIZADO'),
            #         distribuidor=Distribuidor.objects.get(vd_code__iexact='VD00'))

    return True
