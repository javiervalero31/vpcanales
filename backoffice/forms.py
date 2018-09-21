from django import forms
from datetime import date
import datetime
archivo = (
('E', 'Escaladas'),
('R', 'Resueltas'),
)
y = [x for x in range(2017,2026)]
class UploadFileForm(forms.Form):

    file = forms.FileField(label='Archivo que desea subir')
    date = forms.DateField(label='Fecha del Insumo',widget=forms.SelectDateWidget(years=y), initial=datetime.date.today)
    tipo = forms.CharField(label='Seleccione el tipo de archivo', widget=forms.Select(choices=archivo))
