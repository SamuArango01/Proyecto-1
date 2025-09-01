# car2data_project/apps/forms_generation/views.py

import os
from datetime import datetime
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from .models import GeneratedForm, ContratoMandato, ContratoCompraventa, FormularioTramite
from .forms import (ContratoMandatoForm, ContratoCompraventaForm, FormularioTramiteForm, 
                   DocumentSelectionForm)
from apps.documents.models import Document
from apps.vehicles.models import Vehiculo, Persona
from services.DocumentGenerator import DocumentGenerator
import logging

logger = logging.getLogger(__name__)

class FormSelectionView(LoginRequiredMixin, TemplateView):
    template_name = 'forms_generation/form_selection.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        document_id = self.request.GET.get('document_id')
        
        if document_id:
            try:
                document = Document.objects.get(id=document_id, user=self.request.user)
                context['document'] = document
                context['extracted_data'] = document.get_structured_data()
                context['form'] = DocumentSelectionForm(initial={'document_id': document_id})
            except Document.DoesNotExist:
                messages.error(self.request, 'Documento no encontrado.')
                return redirect('documents:dashboard')
        
        return context

class GenerateFormView(LoginRequiredMixin, TemplateView):
    template_name = 'forms_generation/generate_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        document_id = self.request.GET.get('document_id')
        form_type = self.request.GET.get('form_type')
        
        if not document_id or not form_type:
            messages.error(self.request, 'Parámetros faltantes.')
            return redirect('forms_generation:forms')
        
        try:
            document = Document.objects.get(id=document_id, user=self.request.user)
            context['document'] = document
            context['form_type'] = form_type
            context['extracted_data'] = document.get_structured_data()

            logger.debug(f"Extracted Data for GenerateFormView: {context['extracted_data']}")

            # Crear o obtener vehículo y persona
            vehiculo = document.get_or_create_vehiculo()
            propietario = document.get_or_create_persona()

            logger.debug(f"Persona (propietario) for GenerateFormView: {propietario.__dict__ if propietario else 'None'}")

            context['vehiculo'] = vehiculo
            context['propietario'] = propietario
            
            # Inicializar formulario según el tipo
            if form_type == 'contrato_mandato':
                form = ContratoMandatoForm()
                # Pre-llenar datos del mandante con el propietario
                if propietario:
                    form.initial.update({
                        'mandante_nombre': propietario.nombre,
                        'mandante_documento': propietario.numero_documento,
                        'mandante_direccion': propietario.direccion,
                        'mandante_telefono': propietario.telefono,
                        'mandante_ciudad': propietario.ciudad,
                    })
                context['form'] = form
                
            elif form_type == 'contrato_compraventa':
                form = ContratoCompraventaForm()
                # Pre-llenar datos del vendedor con el propietario
                if propietario:
                    form.initial.update({
                        'vendedor_nombre': propietario.nombre,
                        'vendedor_documento': propietario.numero_documento,
                        'vendedor_direccion': propietario.direccion,
                        'vendedor_telefono': propietario.telefono,
                        'vendedor_ciudad': propietario.ciudad,
                    })
                context['form'] = form
                
            elif form_type == 'formulario_tramite':
                form = FormularioTramiteForm()
                context['form'] = form
                
        except Document.DoesNotExist:
            messages.error(self.request, 'Documento no encontrado.')
            return redirect('documents:dashboard')
            
        return context
    
    def post(self, request, *args, **kwargs):
        document_id = request.POST.get('document_id')
        form_type = request.POST.get('form_type')
        
        try:
            document = Document.objects.get(id=document_id, user=request.user)
            
            if form_type == 'contrato_mandato':
                return self._process_contrato_mandato(request, document)
            elif form_type == 'contrato_compraventa':
                return self._process_contrato_compraventa(request, document)
            elif form_type == 'formulario_tramite':
                return self._process_formulario_tramite(request, document)
            else:
                messages.error(request, 'Tipo de formulario no válido.')
                return redirect('forms_generation:forms')
                
        except Document.DoesNotExist:
            messages.error(request, 'Documento no encontrado.')
            return redirect('documents:dashboard')
    
    def _process_contrato_mandato(self, request, document):
        """Procesa la generación del contrato de mandato"""
        form = ContratoMandatoForm(request.POST)
        
        if form.is_valid():
            try:
                # Obtener o crear vehículo y personas
                vehiculo = document.get_or_create_vehiculo()
                
                # Crear/obtener mandante
                mandante, created = Persona.objects.get_or_create(
                    numero_documento=form.cleaned_data['mandante_documento'],
                    defaults={
                        'nombre': form.cleaned_data['mandante_nombre'],
                        'direccion': form.cleaned_data.get('mandante_direccion', ''),
                        'telefono': form.cleaned_data.get('mandante_telefono', ''),
                        'ciudad': form.cleaned_data.get('mandante_ciudad', ''),
                        'tipo_documento': 'CC'
                    }
                )
                
                # Crear/obtener mandatario
                mandatario, created = Persona.objects.get_or_create(
                    numero_documento=form.cleaned_data['mandatario_documento'],
                    defaults={
                        'nombre': form.cleaned_data['mandatario_nombre'],
                        'direccion': form.cleaned_data.get('mandatario_direccion', ''),
                        'telefono': form.cleaned_data.get('mandatario_telefono', ''),
                        'ciudad': form.cleaned_data.get('mandatario_ciudad', ''),
                        'tipo_documento': 'CC'
                    }
                )
                
                # Crear el contrato
                contrato = form.save(commit=False)
                contrato.id_vehiculo = vehiculo
                contrato.id_mandante = mandante
                contrato.id_mandatario = mandatario
                contrato.save()
                
                # Generar PDF
                success = self._generate_pdf_document(document, 'contrato_mandato', {
                    'mandante': {
                        'nombre': mandante.nombre,
                        'documento': mandante.numero_documento,
                        'direccion': mandante.direccion,
                        'telefono': mandante.telefono,
                        'ciudad': mandante.ciudad
                    },
                    'mandatario': {
                        'nombre': mandatario.nombre,
                        'documento': mandatario.numero_documento,
                        'direccion': mandatario.direccion,
                        'telefono': mandatario.telefono,
                        'ciudad': mandatario.ciudad
                    },
                    'contrato_id': contrato.id_contrato
                })
                
                if success:
                    messages.success(request, 'Contrato de mandato generado exitosamente.')
                    return redirect('forms_generation:download', form_id=success)
                else:
                    messages.error(request, 'Error al generar el PDF del contrato.')
                    
            except Exception as e:
                logger.error(f"Error procesando contrato de mandato: {str(e)}")
                messages.error(request, 'Error al procesar el contrato.')
        else:
            messages.error(request, 'Formulario con errores. Revisa los datos.')
        
        # Si hay errores, volver a mostrar el formulario
        return render(request, 'forms_generation/generate_form.html', {
            'document': document,
            'form_type': 'contrato_mandato',
            'form': form,
            'extracted_data': document.get_structured_data()
        })
    
    def _process_contrato_compraventa(self, request, document):
        """Procesa la generación del contrato de compraventa"""
        form = ContratoCompraventaForm(request.POST)
        
        if form.is_valid():
            try:
                # Obtener o crear vehículo
                vehiculo = document.get_or_create_vehiculo()
                
                # Crear/obtener vendedor
                vendedor, created = Persona.objects.get_or_create(
                    numero_documento=form.cleaned_data['vendedor_documento'],
                    defaults={
                        'nombre': form.cleaned_data['vendedor_nombre'],
                        'direccion': form.cleaned_data.get('vendedor_direccion', ''),
                        'telefono': form.cleaned_data.get('vendedor_telefono', ''),
                        'ciudad': form.cleaned_data.get('vendedor_ciudad', ''),
                        'tipo_documento': 'CC'
                    }
                )
                
                # Si el vendedor ya existe, actualizar sus datos
                if not created:
                    vendedor.nombre = form.cleaned_data['vendedor_nombre']
                    vendedor.direccion = form.cleaned_data.get('vendedor_direccion', '')
                    vendedor.telefono = form.cleaned_data.get('vendedor_telefono', '')
                    vendedor.ciudad = form.cleaned_data.get('vendedor_ciudad', '')
                    vendedor.save()
                
                # Crear/obtener comprador
                comprador, created = Persona.objects.get_or_create(
                    numero_documento=form.cleaned_data['comprador_documento'],
                    defaults={
                        'nombre': form.cleaned_data['comprador_nombre'],
                        'direccion': form.cleaned_data.get('comprador_direccion', ''),
                        'telefono': form.cleaned_data.get('comprador_telefono', ''),
                        'ciudad': form.cleaned_data.get('comprador_ciudad', ''),
                        'tipo_documento': 'CC'
                    }
                )
                
                # Crear el contrato
                contrato = form.save(commit=False)
                contrato.id_vehiculo = vehiculo
                contrato.id_vendedor = vendedor
                contrato.id_comprador = comprador
                contrato.save()
                
                # Usar los datos del formulario en lugar de los de la base de datos
                # para asegurar que se usen los valores más recientes
                vendedor_info = {
                    'nombre': form.cleaned_data['vendedor_nombre'],
                    'documento': form.cleaned_data['vendedor_documento'],
                    'direccion': form.cleaned_data.get('vendedor_direccion', 'No especificada'),
                    'telefono': form.cleaned_data.get('vendedor_telefono', 'No especificado'),
                    'ciudad': form.cleaned_data.get('vendedor_ciudad', 'No especificada')
                }
                
                # Debug: Mostrar los datos que se están usando
                logger.info(f"Datos del vendedor para el PDF: {vendedor_info}")
                
                # Generar PDF
                success = self._generate_pdf_document(document, 'contrato_compraventa', {
                    'vendedor': vendedor_info,
                    'comprador': {
                        'nombre': comprador.nombre,
                        'documento': comprador.numero_documento,
                        'direccion': comprador.direccion if comprador.direccion else 'No especificada',
                        'telefono': comprador.telefono if comprador.telefono else 'No especificado',
                        'ciudad': comprador.ciudad if comprador.ciudad else 'No especificada'
                    },
                    'valor_venta': contrato.valor_venta,
                    'contrato_id': contrato.id_contrato
                })
                
                if success:
                    messages.success(request, 'Contrato de compraventa generado exitosamente.')
                    return redirect('forms_generation:download', form_id=success)
                else:
                    messages.error(request, 'Error al generar el PDF del contrato.')
                    
            except Exception as e:
                logger.error(f"Error procesando contrato de compraventa: {str(e)}")
                messages.error(request, 'Error al procesar el contrato.')
        else:
            messages.error(request, 'Formulario con errores. Revisa los datos.')
        
        # Si hay errores, volver a mostrar el formulario
        return render(request, 'forms_generation/generate_form.html', {
            'document': document,
            'form_type': 'contrato_compraventa',
            'form': form,
            'extracted_data': document.get_structured_data()
        })
    
    def _process_formulario_tramite(self, request, document):
        """Procesa la generación del formulario de trámite"""
        form = FormularioTramiteForm(request.POST)
        
        if form.is_valid():
            try:
                # Obtener o crear vehículo y propietario
                vehiculo = document.get_or_create_vehiculo()
                propietario = document.get_or_create_persona()
                
                # Crear el formulario de trámite
                formulario = form.save(commit=False)
                formulario.id_vehiculo = vehiculo
                formulario.id_propietario = propietario
                formulario.save()
                
                # Generar PDF
                success = self._generate_pdf_document(document, 'formulario_tramite', {
                    'formulario_id': formulario.id_formulario,
                    'propietario': {
                        'nombre': propietario.nombre,
                        'documento': propietario.numero_documento,
                        'direccion': propietario.direccion,
                        'telefono': propietario.telefono,
                        'ciudad': propietario.ciudad,
                    }
                })
                
                if success:
                    messages.success(request, 'Formulario de trámite generado exitosamente.')
                    return redirect('forms_generation:download', form_id=success)
                else:
                    messages.error(request, 'Error al generar el PDF del formulario.')
                    
            except Exception as e:
                logger.error(f"Error procesando formulario de trámite: {str(e)}")
                messages.error(request, 'Error al procesar el formulario.')
        else:
            messages.error(request, 'Formulario con errores. Revisa los datos.')
        
        # Si hay errores, volver a mostrar el formulario
        return render(request, 'forms_generation/generate_form.html', {
            'document': document,
            'form_type': 'formulario_tramite',
            'form': form,
            'extracted_data': document.get_structured_data()
        })
    
    def _generate_pdf_document(self, document, form_type, additional_data=None):
        """Genera el documento PDF usando el servicio DocumentGenerator"""
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'generated_forms'), exist_ok=True)
            
            generator = DocumentGenerator()
            extracted_data = document.get_structured_data()
            
            # Generar nombre único para el archivo
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{form_type}_{document.id}_{timestamp}.pdf"
            file_path = os.path.join(settings.MEDIA_ROOT, 'generated_forms', filename)
            
            success = False
            
            logger.info(f"Datos extraídos del documento: {extracted_data}")
            
            if form_type == 'contrato_mandato':
                success = generator.generate_contrato_mandato(
                    extracted_data,  # Pasar todo el diccionario de datos extraídos
                    additional_data.get('mandante', {}),
                    additional_data.get('mandatario', {}),
                    file_path
                )
            elif form_type == 'contrato_compraventa':
                success = generator.generate_contrato_compraventa(
                    extracted_data,  # Pasar todo el diccionario de datos extraídos
                    additional_data.get('vendedor', {}),
                    additional_data.get('comprador', {}),
                    additional_data.get('valor_venta'),
                    file_path
                )
            elif form_type == 'formulario_tramite':
                # Crear un diccionario con la estructura esperada por generate_formulario_tramite
                tramite_data = {
                    'vehiculo': extracted_data.get('vehiculo', {}),
                    'propietario': additional_data.get('propietario', {})
                }
                logger.info(f"Datos para formulario de trámite: {tramite_data}")
                success = generator.generate_formulario_tramite(tramite_data, file_path)
            
            if success:
                # Crear registro del formulario generado
                generated_form = GeneratedForm.objects.create(
                    user=document.user,
                    document=document,
                    form_type=form_type,
                    generated_file=f'generated_forms/{filename}'
                )
                
                logger.info(f"Documento PDF generado exitosamente: {file_path}")
                return generated_form.id
            else:
                logger.error(f"Fallo en la generación del PDF: {form_type}")
                return None
                
        except Exception as e:
            logger.error(f"Error generando documento PDF: {str(e)}")
            logger.exception("Detalles del error:")
            return None

class DownloadFormView(LoginRequiredMixin, TemplateView):
    template_name = 'forms_generation/descarga.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_id = kwargs.get('form_id')
        
        try:
            generated_form = GeneratedForm.objects.get(id=form_id, user=self.request.user)
            context['generated_form'] = generated_form
            context['download_url'] = generated_form.generated_file.url if generated_form.generated_file else None
        except GeneratedForm.DoesNotExist:
            messages.error(self.request, 'Formulario no encontrado.')
            return redirect('forms_generation:forms')
        
        return context

class DownloadPDFView(LoginRequiredMixin, TemplateView):
    """Vista para descargar el PDF generado"""
    
    def get(self, request, form_id):
        try:
            generated_form = GeneratedForm.objects.get(id=form_id, user=request.user)
            
            if not generated_form.generated_file:
                raise Http404("Archivo no encontrado")
            
            file_path = generated_form.generated_file.path
            
            if not os.path.exists(file_path):
                raise Http404("Archivo no encontrado en el sistema")
            
            with open(file_path, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                filename = os.path.basename(file_path)
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
                
        except GeneratedForm.DoesNotExist:
            raise Http404("Formulario no encontrado")
        except Exception as e:
            logger.error(f"Error descargando PDF: {str(e)}")
            messages.error(request, 'Error al descargar el archivo.')
            return redirect('forms_generation:forms')

class FormHistoryView(LoginRequiredMixin, ListView):
    model = GeneratedForm
    template_name = 'forms_generation/history.html'
    context_object_name = 'generated_forms'
    paginate_by = 10
    
    def get_queryset(self):
        # Obtener los últimos 30 días de formularios generados
        thirty_days_ago = timezone.now() - timedelta(days=30)
        return GeneratedForm.objects.filter(
            user=self.request.user,
            created_at__gte=thirty_days_ago
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'history'
        return context

# Vista API para obtener datos de vista previa
class PreviewDataView(LoginRequiredMixin, TemplateView):
    """Vista para obtener datos de vista previa via AJAX"""
    
    def get(self, request):
        document_id = request.GET.get('document_id')
        form_type = request.GET.get('form_type')
        
        if not document_id:
            return JsonResponse({'error': 'Document ID requerido'}, status=400)
        
        try:
            document = Document.objects.get(id=document_id, user=request.user)
            extracted_data = document.get_structured_data()
            
            # Estructurar datos según el tipo de formulario
            preview_data = {
                'vehiculo': extracted_data.get('vehiculo', {}),
                'propietario': extracted_data.get('propietario', {}),
                'registro': extracted_data.get('registro', {}),
                'document_name': document.name,
                'document_status': document.status
            }
            
            return JsonResponse({
                'success': True,
                'data': preview_data
            })
            
        except Document.DoesNotExist:
            return JsonResponse({'error': 'Documento no encontrado'}, status=404)
        except Exception as e:
            logger.error(f"Error obteniendo datos de vista previa: {str(e)}")
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)