from django.db import models
from django.contrib.auth.models import User
import json

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('registration', 'Registro Vehicular'),
        ('insurance', 'Seguro'),
        ('inspection', 'Inspección'),
        ('ownership', 'Tarjeta de Propiedad'),
        ('unknown', 'No identificado'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('processing', 'Procesando'),
        ('completed', 'Completado'),
        ('error', 'Error'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES, default='unknown')
    file = models.FileField(upload_to='uploads/pdfs/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    # Campos para información extraída por Gemini
    extracted_data_json = models.TextField(blank=True, null=True)
    extraction_error = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
    def get_extracted_data(self):
        """Retorna los datos extraídos como diccionario"""
        if self.extracted_data_json:
            try:
                return json.loads(self.extracted_data_json)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_extracted_data(self, data_dict):
        """Guarda los datos extraídos como JSON"""
        self.extracted_data_json = json.dumps(data_dict, ensure_ascii=False, indent=2)
        self.save()
    
    def get_absolute_url(self):
        """URL para redirección después de crear/actualizar"""
        from django.urls import reverse
        return reverse('documents:data_preview', kwargs={'pk': self.pk})

class ExtractedData(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    
    # Datos del vehículo
    license_plate = models.CharField(max_length=10, blank=True)
    vin = models.CharField(max_length=17, blank=True)
    make = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=50, blank=True)
    year = models.IntegerField(null=True, blank=True)
    color = models.CharField(max_length=30, blank=True)
    
    # Datos del propietario
    owner_name = models.CharField(max_length=200, blank=True)
    owner_document = models.CharField(max_length=20, blank=True)
    owner_address = models.TextField(blank=True)
    owner_phone = models.CharField(max_length=15, blank=True)
    owner_email = models.EmailField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)