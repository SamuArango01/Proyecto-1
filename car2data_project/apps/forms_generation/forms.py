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
    # Datos del Propietario
    propietario_primer_apellido = forms.CharField(max_length=50, label="Primer Apellido del Propietario", widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'placeholder': 'Primer Apellido'}))
    propietario_segundo_apellido = forms.CharField(max_length=50, label="Segundo Apellido del Propietario", required=False, widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'placeholder': 'Segundo Apellido'}))
    propietario_nombres = forms.CharField(max_length=100, label="Nombres del Propietario", widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'placeholder': 'Nombres'}))
    propietario_documento = forms.CharField(max_length=20, label="Documento del Propietario", widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'placeholder': 'Número de documento'}))
    propietario_direccion = forms.CharField(max_length=100, label="Dirección del Propietario", widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'placeholder': 'Dirección'}))
    propietario_ciudad = forms.CharField(max_length=50, label="Ciudad del Propietario", widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'placeholder': 'Ciudad'}))
    propietario_telefono = forms.CharField(max_length=20, label="Teléfono del Propietario", widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'placeholder': 'Teléfono'}))

    # Datos del Comprador
    comprador_primer_apellido = forms.CharField(max_length=50, label="Primer Apellido del Comprador", required=False, widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'placeholder': 'Primer Apellido'}))
    comprador_segundo_apellido = forms.CharField(max_length=50, label="Segundo Apellido del Comprador", required=False, widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'placeholder': 'Segundo Apellido'}))
    comprador_nombres = forms.CharField(max_length=100, label="Nombres del Comprador", required=False, widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'placeholder': 'Nombres'}))
    comprador_documento = forms.CharField(max_length=20, label="Documento del Comprador", required=False, widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'placeholder': 'Número de documento'}))
    comprador_direccion = forms.CharField(max_length=100, label="Dirección del Comprador", required=False, widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'placeholder': 'Dirección'}))
    comprador_ciudad = forms.CharField(max_length=50, label="Ciudad del Comprador", required=False, widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'placeholder': 'Ciudad'}))
    comprador_telefono = forms.CharField(max_length=20, label="Teléfono del Comprador", required=False, widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'placeholder': 'Teléfono'}))

    # Datos del Vehículo
    marca = forms.CharField(max_length=50, label="Marca", widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'}))
    linea = forms.CharField(max_length=50, label="Línea", widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'}))
    color = forms.CharField(max_length=50, label="Color", widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'}))
    modelo = forms.CharField(max_length=4, label="Modelo", widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'}))
    cilindrada = forms.CharField(max_length=10, label="Cilindrada", widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'}))
    capacidad = forms.CharField(max_length=10, label="Capacidad", widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'}))
    potencia = forms.CharField(max_length=10, label="Potencia", widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'}))
    carroceria = forms.CharField(max_length=50, label="Carrocería", widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'}))
    numero_motor = forms.CharField(max_length=50, label="Número de Motor", widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'}))
    numero_chasis = forms.CharField(max_length=50, label="Número de Chasis", widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'}))
    numero_serie = forms.CharField(max_length=50, label="Número de Serie", widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'}))
    numero_vin = forms.CharField(max_length=50, label="Número VIN", widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'}))
    observaciones = forms.CharField(widget=forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'rows': 3}), required=False, label="Observaciones")

    # Campos de importación
    declaracion_importacion = forms.CharField(max_length=100, label="Declaración de Importación", required=False, widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'}))
    fecha_importacion = forms.CharField(max_length=50, label="Fecha de Importación", required=False, widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'}))

    class Meta:
        model = FormularioTramite
        fields = [
            'propietario_primer_apellido', 'propietario_segundo_apellido', 'propietario_nombres', 'propietario_documento',
            'propietario_direccion', 'propietario_ciudad', 'propietario_telefono',
            'comprador_primer_apellido', 'comprador_segundo_apellido', 'comprador_nombres', 'comprador_documento',
            'comprador_direccion', 'comprador_ciudad', 'comprador_telefono',
            'marca', 'linea', 'color', 'modelo', 'cilindrada', 'capacidad', 'potencia', 'carroceria',
            'numero_motor', 'numero_chasis', 'numero_serie', 'numero_vin',
            'tipo_servicio', 'fecha_tramite', 'observaciones',
            'declaracion_importacion', 'fecha_importacion'
        ]
        widgets = {
            'tipo_servicio': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'}),
            'fecha_tramite': forms.DateInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'type': 'date'}),
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