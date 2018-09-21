from django import forms
from django.forms import ModelForm
from .models import *
from django.forms import ModelChoiceField
from django.contrib.admin import widgets


meses = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']

class filtro(forms.Form):
    tipo = forms.ModelChoiceField(queryset = Tipo.objects.all(),to_field_name="tipo",required=False)
    # region = forms.ModelChoiceField(queryset = Region.objects.all(),to_field_name="region",required=False)
    lider = forms.ModelChoiceField(queryset = Lider.objects.all().order_by('lider'),to_field_name="lider",required=False)
    codigo = forms.CharField(required=False)
    def __init__(self,*args,**kwargs):
        super(filtro,self).__init__(*args,**kwargs)
        for f in self.fields.items():
            self.fields[f[0]].widget.attrs["class"] = 'form-control'





class editar(ModelForm):
    def __init__(self, *args, **kwargs):
        super(editar, self).__init__(*args,**kwargs)
        #Se le agrega estilos a los campos
        for f in self.fields.items():
            if (f[0] in meses) or (f[0] == 'punto_rojo'):
                continue
            else:
                self.fields[f[0]].widget.attrs["class"] = 'form-control'
        #Se agregan validaciones para el formulario
        self.fields['codigo_unico'].widget.attrs["readonly"] = True
        self.fields['correo_tienda'].widget.attrs["data-validation"] = "email"
        self.fields['correo_empresario'].widget.attrs["data-validation"] = "email"
        self.fields['telefono_tienda'].widget.attrs["data-validation"] = "number"
        self.fields['telefono_empresario'].widget.attrs["data-validation"] = "number"
        self.fields['telefono_tienda'].widget.attrs["data-validation-help"] = "04141234567 Sin parentesis, ni guiones"
        self.fields['telefono_tienda'].widget.attrs["pattern"] = "[0-9]{11}"
        self.fields['telefono_empresario'].widget.attrs["data-validation-help"] = "04141234567 Sin parentesis, ni guiones"
        self.fields['telefono_empresario'].widget.attrs["pattern"] = "[0-9]{11}"
        self.fields['hora_apertura'].widget.attrs["data-validation-help"] = "09:00:00 HH:MM:SS Sistema horario 24 Horas"
        self.fields['hora_apertura'].widget.attrs["data-validation-regexp"] = "/^\d?\d(?::\d{2}){2}$/"
        self.fields['hora_cierre'].widget.attrs["data-validation-help"] = "14:00:00 HH:MM:SS Sistema horario 24 Horas"
        self.fields['hora_cierre'].widget.attrs["data-validation-regexp"] = "/^\d?\d(?::\d{2}){2}$/"
        self.fields['persona_contacto'].widget.attrs["data-validation-regexp"] = "[A-Z\s]"
        self.fields['persona_contacto'].widget.attrs["data-validation"] = "custom"
        self.fields['persona_contacto'].widget.attrs["style"] = "text-transform:uppercase"
        self.fields['ldap'].required = False #JV

    class Meta:
        model = Temporal
        fields = '__all__'
        labels = {	"municipio_key":"Municipio",
        	"estado_key":"Estado",
        	"tipo_key":"Tipo",
        	"tipo_aa_key":"Tipo AA",
        	"oficina_key":"Oficina",
        	"codigo_deudor_key":"Codigo Deudor",
        	"nombre_key":"Nombre",
        	"direccion_key":"Direccion",
        	"region_key":"Region",
        	"coordinador_key":"Coordinador",
        	"lider_key":"Lider",
        	"gerente_key":"Gerente",
        	"centro_recarga_key":"Centro Recarga",
        	"distribuidor_key":"Distribuidor",
        	"status_key":"Status",
        	"rif_key":"Rif",
        }

class agregar_tienda(ModelForm):
    def __init__(self, *args, **kwargs):
        super(agregar_tienda, self).__init__(*args,**kwargs)
        #Se le agrega estilos a los campos
        for f in self.fields.items():
            if (f[0] in meses) or (f[0] == 'punto_rojo'):
                continue
            else:
                self.fields[f[0]].widget.attrs["class"] = 'form-control'
        #Se agregan validaciones para el formulario
        # self.fields['codigo_unico'].widget.attrs["readonly"] = True
        self.fields['correo_tienda'].widget.attrs["data-validation"] = "email"
        self.fields['correo_empresario'].widget.attrs["data-validation"] = "email"
        self.fields['telefono_tienda'].widget.attrs["data-validation"] = "number"
        self.fields['telefono_empresario'].widget.attrs["data-validation"] = "number"
        self.fields['telefono_tienda'].widget.attrs["data-validation-help"] = "04141234567 Sin parentesis, ni guiones"
        self.fields['telefono_tienda'].widget.attrs["pattern"] = "[0-9]{11}"
        self.fields['telefono_empresario'].widget.attrs["data-validation-help"] = "04141234567 Sin parentesis, ni guiones"
        self.fields['telefono_empresario'].widget.attrs["pattern"] = "[0-9]{11}"
        self.fields['hora_apertura'].widget.attrs["data-validation-help"] = "09:00:00 HH:MM:SS Sistema horario 24 Horas"
        self.fields['hora_apertura'].widget.attrs["data-validation-regexp"] = "/^\d?\d(?::\d{2}){2}$/"
        self.fields['hora_cierre'].widget.attrs["data-validation-help"] = "14:00:00 HH:MM:SS Sistema horario 24 Horas"
        self.fields['hora_cierre'].widget.attrs["data-validation-regexp"] = "/^\d?\d(?::\d{2}){2}$/"
        self.fields['persona_contacto'].widget.attrs["data-validation-regexp"] = "[A-Z\s]"
        self.fields['persona_contacto'].widget.attrs["data-validation"] = "custom"
        self.fields['persona_contacto'].widget.attrs["style"] = "text-transform:uppercase"

    class Meta:
        model = Temporal
        fields = '__all__'
        exclude = ['ldap']
        labels = {	"municipio_key":"Municipio",
        	"estado_key":"Estado",
        	"tipo_key":"Tipo",
        	"tipo_aa_key":"Tipo AA",
        	"oficina_key":"Oficina",
        	"codigo_deudor_key":"Codigo Deudor",
        	"nombre_key":"Nombre",
        	"direccion_key":"Direccion",
        	"region_key":"Region",
        	"coordinador_key":"Coordinador",
        	"lider_key":"Lider",
        	"gerente_key":"Gerente",
        	"centro_recarga_key":"Centro Recarga",
        	"distribuidor_key":"Distribuidor",
        	"status_key":"Status",
        	"rif_key":"Rif",
        }



class aprobar_original(ModelForm):
    def __init__(self, *args, **kwargs):
        super(aprobar_original, self).__init__(*args,**kwargs)
        for f in self.fields.items():
            if (f[0] in meses) or (f[0] == 'punto_rojo'):
                self.fields[f[0]].widget.attrs["onclick"] = "return false;"
            else:
                self.fields[f[0]].widget.attrs["class"] = 'form-control'
                self.fields[f[0]].widget.attrs["readonly"] = True
    class Meta:
        model = Temporal
        fields= '__all__'
        exclude = ['ldap']

class aprobar_cambio(ModelForm):
    def __init__(self, *args, **kwargs):
        super(aprobar_cambio, self).__init__(*args,**kwargs)
        for f in self.fields.items():
            if (f[0] in meses) or (f[0] == 'punto_rojo'):
                self.fields[f[0]].widget.attrs["onclick"] = "return false;"
            else:
                self.fields[f[0]].widget.attrs["class"] = 'form-control'
                self.fields[f[0]].widget.attrs["readonly"] = True
    class Meta:
        model = Cambio
        fields= '__all__'
        exclude = ('aprobacion_1','aprobacion_2','rechazado','idop_solicitante')

class descarga(forms.Form):
    fecha = forms.ModelChoiceField(queryset=Historico.objects.values_list("fecha",flat=True).distinct().order_by("fecha"))
    def __init__(self, *args, **kwargs):
        super(descarga, self).__init__(*args,**kwargs)
        self.fields['fecha'].widget = forms.Select(attrs={'class':'form-control','onchange': 'this.form.submit();'})
        self.fields['fecha'].queryset = Historico.objects.values_list("fecha",flat=True).distinct().order_by("fecha")

class agregar_valores(forms.Form):
    tipo= forms.CharField(max_length=5,required=False)
    tipo_aa = forms.CharField(max_length=100,required=False)
    oficina = forms.CharField(max_length=25,required=False)
    rif = forms.CharField(max_length=10,required=False)
    codigo_deudor=forms.CharField(max_length=10,required=False)
    nombre=forms.CharField(max_length=100,required=False)
    direccion=forms.CharField(max_length=1000,required=False)
    region=forms.CharField(max_length=25,required=False)
    gerente=forms.CharField(max_length=50,required=False)
    lider=forms.CharField(max_length=50,required=False)
    coordinador=forms.CharField(max_length=50,required=False)
    centro_recarga=forms.CharField(max_length=50,required=False)
    distribuidor=forms.CharField(max_length=200,required=False)
    status=forms.CharField(max_length=200,required=False)
    def __init__(self,*args,**kwargs):
        super(agregar_valores,self).__init__(*args,**kwargs)
        self.fields['rif'].widget.attrs["data-validation-regexp"] = "^([VEJPG]{1})([0-9]{9})$)/"
        for f in self.fields.items():
            self.fields[f[0]].widget.attrs["class"] = 'form-control'
            self.fields[f[0]].widget.attrs["style"] = "text-transform:uppercase"
