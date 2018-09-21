# from django import forms
# from django.forms import ModelForm
# from .models import Insumo


from django import forms
from datetime import date
import datetime


class JerarquiaPlanes(forms.Form):
	jerarquia = forms.FileField(label='Jerarquia y planes que desea subir')

class Actividades(forms.Form):
	activaciones = forms.FileField(label='Activaciones que desea subir')
	altas = forms.FileField(label='Altas que desea subir')


class Bajas(forms.Form):	
	bajas = forms.FileField(label='Bajas que desea subir')



class Cuotas(forms.Form):	
	cuotas = forms.FileField(label='Cuotas que desea subir')