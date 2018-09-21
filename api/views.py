from django.shortcuts import render

import pandas as pd
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from url_filter.integrations.drf import DjangoFilterBackend

from .models import Imei
from .form import UploadFileForm
from .serializers import ImeiSerializer


def upload_imei_data(request):
    """ Load IMEI, Technology data """
    form = UploadFileForm(request.POST, request.FILES)
    if request.method == 'POST':
        Imei.objects.all().delete()
        if form.is_valid():
            ruta_insumo = request.FILES.get('file')

            fields = ['TAC', 'TECHNOLOGY_3G', 'TECHNOLOGY_4G_VE']
            df = pd.read_csv(ruta_insumo, sep='|', usecols=fields)

            df['TECHNOLOGY_3G'] = df['TECHNOLOGY_3G'] \
                .map({'HSPA': True, 'R99': True, 'No': False})
            df['TECHNOLOGY_4G_VE'] = df['TECHNOLOGY_4G_VE'] \
                .map({'LTE': True, 'No LTE': False})

            df['TECNOLOGIA'] = ''

            lista_imei = []
            for row in df.itertuples():
                if row.TECHNOLOGY_4G_VE:
                    df.at[row.Index, 'TECNOLOGIA'] = '4G'
                elif row.TECHNOLOGY_3G:
                    df.at[row.Index, 'TECNOLOGIA'] = '3G'
                else:
                    df.at[row.Index, 'TECNOLOGIA'] = '2G'

            for row in df.itertuples():
                lista_imei.append(Imei(imei=row.TAC, tecnologia=row.TECNOLOGIA))
                print(Imei(imei=row.TAC, tecnologia=row.TECNOLOGIA))

            Imei.objects.bulk_create(lista_imei)
            print(len(lista_imei))
            return render(request, 'upload.html', {'form': form})
    else:
        return render(request, 'upload.html', {'form': form})


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class ImeiList(generics.ListAPIView):
    """ API endpoint for listing and creating Imei objects """
    queryset = Imei.objects.all().order_by('imei')
    filter_backends = [DjangoFilterBackend]
    pagination_class = LargeResultsSetPagination
    filter_fields = ['imei', 'tecnologia']
    serializer_class = ImeiSerializer
