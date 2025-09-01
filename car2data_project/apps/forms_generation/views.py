from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime
from .models import GeneratedForm
from apps.documents.models import Document, ExtractedData

class FormSelectionView(LoginRequiredMixin, TemplateView):
    template_name = 'forms_generation/form_selection.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        document_id = self.request.GET.get('document_id') or self.request.POST.get('document_id')
        if document_id:
            context['document'] = get_object_or_404(
                Document, id=document_id, user=self.request.user
            )
        return context
    
    def post(self, request, *args, **kwargs):
        # Procesar datos del form data_preview
        document_id = request.POST.get('document_id')
        document = get_object_or_404(Document, id=document_id, user=request.user)
        
        # Actualizar datos extraídos con la nueva estructura
        extracted_data, created = ExtractedData.objects.get_or_create(document=document)
        
        # Información del vehículo
        extracted_data.license_plate = request.POST.get('placa', '')
        extracted_data.make = request.POST.get('marca', '')
        extracted_data.model = request.POST.get('linea', '')
        extracted_data.year = self._parse_int_field(request.POST.get('modelo', ''))
        extracted_data.color = request.POST.get('color', '')
        extracted_data.vin = request.POST.get('vin', '')
        
        # Información del propietario
        extracted_data.owner_name = request.POST.get('propietario_nombre', '')
        extracted_data.owner_id = request.POST.get('propietario_identificacion', '')
        
        # Información técnica del vehículo (campos adicionales que podrían existir en el modelo)
        # Estos campos se pueden agregar al modelo ExtractedData si no existen
        if hasattr(extracted_data, 'engine_number'):
            extracted_data.engine_number = request.POST.get('numero_motor', '')
        if hasattr(extracted_data, 'chassis_number'):
            extracted_data.chassis_number = request.POST.get('numero_chasis', '')
        if hasattr(extracted_data, 'vehicle_class'):
            extracted_data.vehicle_class = request.POST.get('clase_vehiculo', '')
        if hasattr(extracted_data, 'body_type'):
            extracted_data.body_type = request.POST.get('tipo_carroceria', '')
        if hasattr(extracted_data, 'cylinder_capacity'):
            extracted_data.cylinder_capacity = request.POST.get('cilindrada_cc', '')
        if hasattr(extracted_data, 'fuel_type'):
            extracted_data.fuel_type = request.POST.get('combustible', '')
        if hasattr(extracted_data, 'service_type'):
            extracted_data.service_type = request.POST.get('servicio', '')
        if hasattr(extracted_data, 'capacity'):
            extracted_data.capacity = request.POST.get('capacidad_kg_psj', '')
        if hasattr(extracted_data, 'power_hp'):
            extracted_data.power_hp = request.POST.get('potencia_hp', '')
        if hasattr(extracted_data, 'doors'):
            extracted_data.doors = self._parse_int_field(request.POST.get('puertas', ''))
        
        # Información de registro
        if hasattr(extracted_data, 'transit_license'):
            extracted_data.transit_license = request.POST.get('licencia_transito_numero', '')
        if hasattr(extracted_data, 'import_declaration'):
            extracted_data.import_declaration = request.POST.get('declaracion_importacion', '')
        if hasattr(extracted_data, 'import_date'):
            extracted_data.import_date = self._parse_date_field(request.POST.get('fecha_importacion', ''))
        if hasattr(extracted_data, 'registration_date'):
            extracted_data.registration_date = self._parse_date_field(request.POST.get('fecha_matricula', ''))
        if hasattr(extracted_data, 'license_issue_date'):
            extracted_data.license_issue_date = self._parse_date_field(request.POST.get('fecha_expedicion_licencia', ''))
        if hasattr(extracted_data, 'transit_authority'):
            extracted_data.transit_authority = request.POST.get('organismo_transito', '')
        
        # Restricciones
        if hasattr(extracted_data, 'mobility_restriction'):
            extracted_data.mobility_restriction = request.POST.get('restriccion_movilidad', '')
        if hasattr(extracted_data, 'armoring'):
            extracted_data.armoring = request.POST.get('blindaje', '')
        if hasattr(extracted_data, 'property_limitation'):
            extracted_data.property_limitation = request.POST.get('limitacion_propiedad', '')
        
        extracted_data.save()
        
        return self.get(request, *args, **kwargs)
    
    def _parse_int_field(self, value):
        """Convierte un string a entero, retorna None si no es válido"""
        try:
            if value and value.strip() and value.strip() != 'No disponible':
                return int(value.strip())
        except (ValueError, AttributeError):
            pass
        return None
    
    def _parse_date_field(self, value):
        """Convierte un string a fecha, retorna None si no es válido"""
        try:
            if value and value.strip() and value.strip() != 'No disponible':
                # Intenta varios formatos de fecha comunes
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d']:
                    try:
                        return datetime.strptime(value.strip(), fmt).date()
                    except ValueError:
                        continue
        except (ValueError, AttributeError):
            pass
        return None


class GenerateFormView(LoginRequiredMixin, TemplateView):
    template_name = 'forms_generation/generate.html'
    
    def post(self, request, *args, **kwargs):
        document_id = request.POST.get('document_id')
        form_type = request.POST.get('form_type')
        
        document = get_object_or_404(Document, id=document_id, user=request.user)
        
        # Simular generación de formulario
        generated_form = GeneratedForm.objects.create(
            user=request.user,
            document=document,
            form_type=form_type
        )
        
        messages.success(request, 'Formulario generado exitosamente')
        return redirect('forms_generation:download', form_id=generated_form.id)


class DownloadFormView(LoginRequiredMixin, TemplateView):
    template_name = 'forms_generation/download.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_id = kwargs['form_id']
        context['generated_form'] = get_object_or_404(
            GeneratedForm, id=form_id, user=self.request.user
        )
        return context