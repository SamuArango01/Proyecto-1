# car2data_project/apps/forms_generation/forms.py

from django import forms
from .models import ContratoCompraventa, ContratoMandato, FormularioTramite
from apps.vehicles.models import Persona, Vehiculo

class ContratoMandatoForm(forms.ModelForm):
    # Campos para el mandante
    mandante_nombre = forms.CharField(
        max_length=100,
        label="Nombre del Mandante",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
            'placeholder': 'Ingrese el nombre completo del mandante'
        })
    )
    mandante_documento = forms.CharField(
        max_length=20,
        label="Documento del Mandante",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
            'placeholder': 'Número de documento'
        })
    )
    mandante_direccion = forms.CharField(
        max_length=100,
        required=False,
        label="Dirección del Mandante",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
            'placeholder': 'Dirección completa'
        })
    )
    mandante_telefono = forms.CharField(
        max_length=20,
        required=False,
        label="Teléfono del Mandante",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
            'placeholder': 'Número de teléfono'
        })
    )
    mandante_ciudad = forms.CharField(
        max_length=50,
        required=False,
        label="Ciudad del Mandante",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
            'placeholder': 'Ciudad de residencia'
        })
    )
    
    # Campos para el mandatario
    mandatario_nombre = forms.CharField(
        max_length=100,
        label="Nombre del Mandatario",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
            'placeholder': 'Ingrese el nombre completo del mandatario'
        })
    )
    mandatario_documento = forms.CharField(
        max_length=20,
        label="Documento del Mandatario",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
            'placeholder': 'Número de documento'
        })
    )
    mandatario_direccion = forms.CharField(
        max_length=100,
        required=False,
        label="Dirección del Mandatario",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
            'placeholder': 'Dirección completa'
        })
    )
    mandatario_telefono = forms.CharField(
        max_length=20,
        required=False,
        label="Teléfono del Mandatario",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
            'placeholder': 'Número de teléfono'
        })
    )
    mandatario_ciudad = forms.CharField(
        max_length=50,
        required=False,
        label="Ciudad del Mandatario",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
            'placeholder': 'Ciudad de residencia'
        })
    )

    class Meta:
        model = ContratoMandato
        fields = ['tramites_autorizados', 'organismo_transito', 'ciudad_contrato', 'fecha_contrato']
        widgets = {
            'tramites_autorizados': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
                'rows': 4,
                'placeholder': 'Describa los trámites autorizados'
            }),
            'organismo_transito': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
                'placeholder': 'Organismo de tránsito'
            }),
            'ciudad_contrato': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
                'placeholder': 'Ciudad donde se firma el contrato'
            }),
            'fecha_contrato': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
                'type': 'date'
            }),
        }

class ContratoCompraventaForm(forms.ModelForm):
    # Campos para el vendedor
    vendedor_nombre = forms.CharField(
        max_length=100,
        label="Nombre del Vendedor",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
            'placeholder': 'Ingrese el nombre completo del vendedor'
        })
    )
    vendedor_documento = forms.CharField(
        max_length=20,
        label="Documento del Vendedor",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
            'placeholder': 'Número de documento'
        })
    )
    vendedor_direccion = forms.CharField(
        max_length=100,
        required=False,
        label="Dirección del Vendedor",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
            'placeholder': 'Dirección completa'
        })
    )
    vendedor_telefono = forms.CharField(
        max_length=20,
        required=False,
        label="Teléfono del Vendedor",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
            'placeholder': 'Número de teléfono'
        })
    )
    vendedor_ciudad = forms.CharField(
        max_length=50,
        required=False,
        label="Ciudad del Vendedor",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
            'placeholder': 'Ciudad de residencia'
        })
    )
    
    # Campos para el comprador
    comprador_nombre = forms.CharField(
        max_length=100,
        label="Nombre del Comprador",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
            'placeholder': 'Ingrese el nombre completo del comprador'
        })
    )
    comprador_documento = forms.CharField(
        max_length=20,
        label="Documento del Comprador",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
            'placeholder': 'Número de documento'
        })
    )
    comprador_direccion = forms.CharField(
        max_length=100,
        required=False,
        label="Dirección del Comprador",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
            'placeholder': 'Dirección completa'
        })
    )
    comprador_telefono = forms.CharField(
        max_length=20,
        required=False,
        label="Teléfono del Comprador",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
            'placeholder': 'Número de teléfono'
        })
    )
    comprador_ciudad = forms.CharField(
        max_length=50,
        required=False,
        label="Ciudad del Comprador",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
            'placeholder': 'Ciudad de residencia'
        })
    )

    class Meta:
        model = ContratoCompraventa
        fields = ['valor_venta', 'valor_venta_letras', 'forma_pago', 'ciudad_contrato', 'fecha_contrato']
        widgets = {
            'valor_venta': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
                'placeholder': 'Valor de venta en números',
                'step': '0.01'
            }),
            'valor_venta_letras': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
                'rows': 3,
                'placeholder': 'Valor de venta en letras'
            }),
            'forma_pago': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
                'rows': 3,
                'placeholder': 'Descripción de la forma de pago'
            }),
            'ciudad_contrato': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
                'placeholder': 'Ciudad donde se firma el contrato'
            }),
            'fecha_contrato': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
                'type': 'date'
            }),
        }

class FormularioTramiteForm(forms.ModelForm):
    class Meta:
        model = FormularioTramite
        fields = ['tipo_servicio', 'fecha_tramite']
        widgets = {
            'tipo_servicio': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise'
            }),
            'fecha_tramite': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
                'type': 'date'
            }),
        }

class DocumentSelectionForm(forms.Form):
    FORM_TYPE_CHOICES = [
        ('', 'Seleccionar tipo de documento'),
        ('contrato_mandato', 'Contrato de Mandato'),
        ('contrato_compraventa', 'Contrato de Compraventa'),
        ('formulario_tramite', 'Formulario de Trámite'),
    ]
    
    form_type = forms.ChoiceField(
        choices=FORM_TYPE_CHOICES,
        label="Tipo de Documento",
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-turquoise focus:border-turquoise',
            'onchange': 'toggleFormFields(this.value)'
        })
    )
    
    document_id = forms.IntegerField(widget=forms.HiddenInput())