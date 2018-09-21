from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Archivo que desea subir')