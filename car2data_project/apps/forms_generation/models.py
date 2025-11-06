from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.vehicles.models import Vehiculo, Persona
from apps.documents.models import Document

class GeneratedForm(models.Model):
    FORM_TYPE_CHOICES = [
        ('contrato_compraventa', 'Contrato de Compraventa'),
        ('contrato_mandato', 'Contrato de Mandato'),
        ('formulario_tramite', 'Formulario de Trámite'),
    ]
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    form_type = models.CharField(max_length=50, choices=FORM_TYPE_CHOICES)
    generated_file = models.FileField(upload_to='generated_forms/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'generated_form'
        verbose_name = 'Formulario Generado'
        verbose_name_plural = 'Formularios Generados'

    def __str__(self):
        return f"Formulario {self.id} - {self.get_form_type_display()}"

    def get_vehicle_display(self):
        try:
            data = self.document.get_structured_data()
            veh = data.get('vehiculo', {}) or {}
            placa = (veh.get('placa') or '').strip()
            marca = (veh.get('marca') or '').strip()
            linea = (veh.get('linea') or '').strip()
            if placa:
                return placa
            label = f"{marca} {linea}".strip()
            if label:
                return label
        except Exception:
            pass
        return self.document.name

class ContratoCompraventa(models.Model):
    id_contrato = models.AutoField(primary_key=True)
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, db_column='id_vehiculo')
    id_vendedor = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='contratos_vendedor', db_column='id_vendedor')
    id_comprador = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='contratos_comprador', db_column='id_comprador')
    valor_venta = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_venta_letras = models.TextField(blank=True)
    forma_pago = models.TextField(blank=True)
    ciudad_contrato = models.CharField(max_length=50, blank=True)
    fecha_contrato = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contrato_compraventa'
        verbose_name = 'Contrato de Compraventa'
        verbose_name_plural = 'Contratos de Compraventa'

    def __str__(self):
        return f"Contrato {self.id_contrato} - {self.id_vehiculo.placa}"

class ContratoMandato(models.Model):
    id_contrato = models.AutoField(primary_key=True)
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, db_column='id_vehiculo')
    id_mandante = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='mandatos_mandante', db_column='id_mandante')
    id_mandatario = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='mandatos_mandatario', db_column='id_mandatario')
    tramites_autorizados = models.TextField(blank=True)
    organismo_transito = models.CharField(max_length=100, blank=True)
    ciudad_contrato = models.CharField(max_length=50, blank=True)
    fecha_contrato = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contrato_mandato'
        verbose_name = 'Contrato de Mandato'
        verbose_name_plural = 'Contratos de Mandato'

    def __str__(self):
        return f"Mandato {self.id_contrato} - {self.id_vehiculo.placa}"

class FormularioTramite(models.Model):
    TIPO_SERVICIO_CHOICES = [
        ('particular', 'Particular'),
        ('publico', 'Público'),
        ('oficial', 'Oficial'),
        ('diplomatico', 'Diplomático'),
    ]
    
    id_formulario = models.AutoField(primary_key=True)
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, db_column='id_vehiculo')
    id_propietario = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='tramites_propietario', db_column='id_propietario')
    id_comprador = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='tramites_comprador', db_column='id_comprador', null=True, blank=True)
    tipo_servicio = models.CharField(max_length=50, choices=TIPO_SERVICIO_CHOICES, default='particular')
    fecha_tramite = models.DateField(default=timezone.now)
    observaciones = models.TextField(blank=True)

    # Datos de importación
    declaracion_importacion = models.CharField(max_length=100, blank=True)
    fecha_importacion = models.CharField(max_length=50, blank=True)
    
    # Campos REG para números de identificación
    reg_numero_motor = models.CharField(max_length=1, blank=True, null=True, help_text="S o N")
    reg_numero_chasis = models.CharField(max_length=1, blank=True, null=True, help_text="S o N")
    reg_numero_serie = models.CharField(max_length=1, blank=True, null=True, help_text="S o N")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'formulario_tramite'
        verbose_name = 'Formulario de Trámite'
        verbose_name_plural = 'Formularios de Trámite'

    def __str__(self):
        return f"Trámite {self.id_formulario} - {self.id_vehiculo.placa}"