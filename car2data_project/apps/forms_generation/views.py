# car2data_project/apps/forms_generation/views.py

import os
from datetime import datetime
from datetime import timedelta
import logging
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, FormView, ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
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
            
            # Inicializar formulario según el tipo y pre-llenar con datos extraídos
            initial_data = {}
            extracted_propietario = context['extracted_data'].get('propietario', {})
            extracted_vehiculo = context['extracted_data'].get('vehiculo', {})

            if form_type == 'contrato_mandato':
                initial_data = {
                    'placa': extracted_vehiculo.get('placa'),
                    'mandante_nombre': extracted_propietario.get('nombre'),
                    'mandante_documento': extracted_propietario.get('identificacion') or extracted_propietario.get('documento'),
                    'mandante_direccion': extracted_propietario.get('direccion'),
                    'mandante_telefono': extracted_propietario.get('telefono'),
                    'mandante_ciudad': extracted_propietario.get('ciudad'),
                    # Fecha por defecto: hoy
                    'fecha_contrato': timezone.now().date().isoformat(),
                }
                context['form'] = ContratoMandatoForm(initial=initial_data)
                
            elif form_type == 'contrato_compraventa':
                initial_data = {
                    'vendedor_nombre': extracted_propietario.get('nombre'),
                    'vendedor_documento': extracted_propietario.get('identificacion') or extracted_propietario.get('documento'),
                    'vendedor_direccion': extracted_propietario.get('direccion'),
                    'vendedor_telefono': extracted_propietario.get('telefono'),
                    'vendedor_ciudad': extracted_propietario.get('ciudad'),
                    # Fecha por defecto: hoy
                    'fecha_contrato': timezone.now().date().isoformat(),
                }
                context['form'] = ContratoCompraventaForm(initial=initial_data)
                
            elif form_type == 'formulario_tramite':
                extracted_propietario = context['extracted_data'].get('propietario', {})
                extracted_registro = context['extracted_data'].get('registro', {})
                # Preferir 'informacion_vehiculo' (como en data_preview), con fallback a 'vehiculo'
                extracted_vehiculo = context['extracted_data'].get('informacion_vehiculo') or context['extracted_data'].get('vehiculo', {})

                # Helper para separar nombre completo en apellidos y nombres
                def split_apellidos_nombres(fullname: str):
                    try:
                        if not fullname:
                            return '', '', ''
                        parts = str(fullname).strip().split()
                        if len(parts) >= 3:
                            return parts[0], parts[1], ' '.join(parts[2:])
                        if len(parts) == 2:
                            return parts[0], '', parts[1]
                        return parts[0], '', ''
                    except Exception:
                        return '', '', ''

                ap1, ap2, nombres = split_apellidos_nombres(extracted_propietario.get('nombre'))

                # Mapeo usando claves de Document.get_structured_data()
                initial_data = {
                    'placa': extracted_vehiculo.get('placa'),
                    # Datos del Propietario (separados automáticamente)
                    'propietario_primer_apellido': ap1,
                    'propietario_segundo_apellido': ap2,
                    'propietario_nombres': nombres,
                    'propietario_documento': extracted_propietario.get('identificacion'),

                    # Datos del Vehículo
                    'marca': extracted_vehiculo.get('marca'),
                    'linea': extracted_vehiculo.get('linea'),
                    'color': extracted_vehiculo.get('color'),
                    'modelo': extracted_vehiculo.get('modelo'),
                    'cilindrada': extracted_vehiculo.get('cilindrada_cc'),
                    'capacidad': extracted_vehiculo.get('capacidad_kg_psj'),
                    'potencia': extracted_vehiculo.get('potencia_hp'),
                    'carroceria': extracted_vehiculo.get('tipo_carroceria'),
                    'numero_motor': extracted_vehiculo.get('numero_motor'),
                    'reg_numero_motor': extracted_vehiculo.get('reg_numero_motor'),
                    'numero_chasis': extracted_vehiculo.get('numero_chasis'),
                    'reg_numero_chasis': extracted_vehiculo.get('reg_numero_chasis'),
                    'numero_serie': extracted_vehiculo.get('numero_serie'),
                    'reg_numero_serie': extracted_vehiculo.get('reg_numero_serie'),
                    'numero_vin': extracted_vehiculo.get('vin'),
                    'tipo_servicio': extracted_vehiculo.get('servicio'),
                    'clase_vehiculo': extracted_vehiculo.get('clase_vehiculo'),
                    'combustible': extracted_vehiculo.get('combustible'),

                    # Datos de importación
                    'declaracion_importacion': extracted_registro.get('declaracion_importacion'),
                    'fecha_importacion': extracted_registro.get('fecha_importacion'),
                }

                # Normalizar valores tipo "No disponible"/None/"N/A" a cadena vacía
                def _normalize_value(v):
                    try:
                        if v is None:
                            return ''
                        s = str(v).strip()
                        if s.lower() in ['no disponible', 'n/a', 'na', 'none', 'null', 'sin dato']:
                            return ''
                        return s
                    except Exception:
                        return ''

                initial_data = {k: _normalize_value(v) for k, v in initial_data.items()}

                # Filtrar claves con valores vacíos para no enviar al formulario
                initial_data_filtered = {k: v for k, v in initial_data.items() if v != ''}

                # Logging a nivel INFO para que aparezca (y tolerante a fechas)
                logging.info(f"Extracted Data: {json.dumps(context['extracted_data'], indent=2, ensure_ascii=False, default=str)}")
                logging.info(f"Initial Data Mapped: {json.dumps(initial_data, indent=2, ensure_ascii=False, default=str)}")
                logging.info(f"Initial Data Filtered: {json.dumps(initial_data_filtered, indent=2, ensure_ascii=False, default=str)}")

                # Fecha por defecto: hoy, si no viene en los datos iniciales
                if not initial_data_filtered.get('fecha_tramite'):
                    initial_data_filtered['fecha_tramite'] = timezone.now().date().isoformat()

                context['form'] = FormularioTramiteForm(initial=initial_data_filtered)
                
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
                
                # Crear/obtener mandatario (o usar mandante si no hay mandatario)
                tiene_mandatario = form.cleaned_data.get('tiene_mandatario')
                if tiene_mandatario:
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
                else:
                    mandatario = mandante
                
                # Crear el contrato
                contrato = form.save(commit=False)
                contrato.id_vehiculo = vehiculo
                contrato.id_mandante = mandante
                contrato.id_mandatario = mandatario
                contrato.save()
                
                # Obtener datos extraídos del vehículo
                extracted_data = document.get_structured_data()
                vehiculo_data = extracted_data.get('vehiculo', {})
                
                # Incluir todos los datos del formulario en el PDF
                pdf_data = {
                    'mandante': {
                        'nombre': form.cleaned_data['mandante_nombre'],
                        'documento': form.cleaned_data['mandante_documento'],
                        'direccion': form.cleaned_data.get('mandante_direccion', ''),
                        'telefono': form.cleaned_data.get('mandante_telefono', ''),
                        'ciudad': form.cleaned_data.get('mandante_ciudad', '')
                    },
                    'mandatario': ({
                        'nombre': form.cleaned_data['mandatario_nombre'],
                        'documento': form.cleaned_data['mandatario_documento'],
                        'direccion': form.cleaned_data.get('mandatario_direccion', ''),
                        'telefono': form.cleaned_data.get('mandatario_telefono', ''),
                        'ciudad': form.cleaned_data.get('mandatario_ciudad', '')
                    } if tiene_mandatario else {
                        'nombre': '',
                        'documento': '',
                        'direccion': '',
                        'telefono': '',
                        'ciudad': ''
                    }),
                    'vehiculo': vehiculo_data,  # Datos completos del vehículo extraídos
                    'placa': vehiculo.placa if vehiculo else vehiculo_data.get('placa', ''),
                    'contrato_id': contrato.id_contrato,
                    'tramites_autorizados': form.cleaned_data.get('tramites_autorizados', ''),
                    'organismo_transito': form.cleaned_data.get('organismo_transito', '') or extracted_data.get('registro', {}).get('organismo_transito', ''),
                    'ciudad_contrato': form.cleaned_data.get('ciudad_contrato', ''),
                    'fecha_contrato': form.cleaned_data.get('fecha_contrato')
                }
                
                logger.info(f"Datos para PDF de contrato de mandato: {pdf_data}")
                
                # Generar PDF con todos los datos
                success = self._generate_pdf_document(document, 'contrato_mandato', pdf_data)
                
                if success:
                    messages.success(request, 'Contrato de mandato generado exitosamente.')
                    return redirect('forms_generation:download', form_id=success)
                else:
                    messages.error(request, 'Error al generar el PDF del contrato.')
                    
            except Exception as e:
                logger.error(f"Error procesando contrato de mandato: {str(e)}")
                messages.error(request, 'Error al procesar el contrato.')
        else:
            logger.error(f"Errores en el contrato de mandato: {form.errors.as_json()}")
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

                comprador_info = {
                    'nombre': form.cleaned_data['comprador_nombre'],
                    'documento': form.cleaned_data['comprador_documento'],
                    'direccion': form.cleaned_data.get('comprador_direccion', 'No especificada'),
                    'telefono': form.cleaned_data.get('comprador_telefono', 'No especificado'),
                    'ciudad': form.cleaned_data.get('comprador_ciudad', 'No especificada')
                }
                
                # Debug: Mostrar los datos que se están usando
                logger.info(f"Datos del vendedor para el PDF: {vendedor_info}")
                logger.info(f"Datos del comprador para el PDF: {comprador_info}")
                
                # Obtener organismo de tránsito de los datos extraídos
                extracted_data = document.get_structured_data()
                organismo_transito = extracted_data.get('registro', {}).get('organismo_transito', '')
                
                # Generar PDF
                success = self._generate_pdf_document(document, 'contrato_compraventa', {
                    'vendedor': vendedor_info,
                    'comprador': comprador_info,
                    'valor_venta': contrato.valor_venta,
                    'forma_pago': form.cleaned_data.get('forma_pago', ''),
                    'ciudad_contrato': form.cleaned_data.get('ciudad_contrato', ''),
                    'fecha_contrato': form.cleaned_data.get('fecha_contrato'),
                    'organismo_transito': organismo_transito,
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
            logger.error(f"Errores en el contrato de compraventa: {form.errors.as_json()}")
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
                # 1. Cargar datos extraídos originalmente como base
                extracted_data = document.get_structured_data()
                # Preferir 'informacion_vehiculo' (como en data_preview), con fallback a 'vehiculo'
                extracted_vehiculo = extracted_data.get('informacion_vehiculo') or extracted_data.get('vehiculo', {})
                extracted_propietario = extracted_data.get('propietario', {})
                extracted_registro = extracted_data.get('registro', {})

                # Helper para separar nombre completo en apellidos y nombres
                def split_apellidos_nombres(fullname: str):
                    try:
                        if not fullname:
                            return '', '', ''
                        parts = str(fullname).strip().split()
                        if len(parts) >= 3:
                            return parts[0], parts[1], ' '.join(parts[2:])
                        if len(parts) == 2:
                            return parts[0], '', parts[1]
                        return parts[0], '', ''
                    except Exception:
                        return '', '', ''

                ap1, ap2, nombres = split_apellidos_nombres(extracted_propietario.get('nombre'))

                # Normalizador reutilizable
                def _normalize_value(v):
                    try:
                        if v is None:
                            return ''
                        s = str(v).strip()
                        if s.lower() in ['no disponible', 'n/a', 'na', 'none', 'null', 'sin dato']:
                            return ''
                        return s
                    except Exception:
                        return ''

                base_data = {
                    'placa': extracted_vehiculo.get('placa'),
                    'marca': _normalize_value(extracted_vehiculo.get('marca')),
                    'linea': _normalize_value(extracted_vehiculo.get('linea')),
                    'color': _normalize_value(extracted_vehiculo.get('color')),
                    'modelo': _normalize_value(extracted_vehiculo.get('modelo')),
                    'cilindrada': _normalize_value(extracted_vehiculo.get('cilindrada_cc')),
                    'capacidad': _normalize_value(extracted_vehiculo.get('capacidad_kg_psj')),
                    'potencia': _normalize_value(extracted_vehiculo.get('potencia_hp')),
                    'carroceria': _normalize_value(extracted_vehiculo.get('tipo_carroceria')),
                    'numero_motor': _normalize_value(extracted_vehiculo.get('numero_motor')),
                    'reg_numero_motor': _normalize_value(extracted_vehiculo.get('reg_numero_motor')),
                    'numero_chasis': _normalize_value(extracted_vehiculo.get('numero_chasis')),
                    'reg_numero_chasis': _normalize_value(extracted_vehiculo.get('reg_numero_chasis')),
                    'numero_serie': _normalize_value(extracted_vehiculo.get('numero_serie')),
                    'reg_numero_serie': _normalize_value(extracted_vehiculo.get('reg_numero_serie')),
                    'numero_vin': _normalize_value(extracted_vehiculo.get('vin')),
                    'tipo_servicio': _normalize_value(extracted_vehiculo.get('servicio')),
                    'clase_vehiculo': _normalize_value(extracted_vehiculo.get('clase_vehiculo')),
                    'combustible': _normalize_value(extracted_vehiculo.get('combustible')),
                    # Propietario (separado automáticamente)
                    'propietario_primer_apellido': ap1,
                    'propietario_segundo_apellido': ap2,
                    'propietario_nombres': nombres,
                    'propietario_documento': _normalize_value(extracted_propietario.get('identificacion')),

                    # Datos de importación
                    'declaracion_importacion': _normalize_value(extracted_registro.get('declaracion_importacion')),
                    'fecha_importacion': _normalize_value(extracted_registro.get('fecha_importacion')),
                }

                # 2. Combinar con datos del formulario (los datos del form tienen prioridad)
                # Se filtran los valores None de cleaned_data para no sobreescribir datos existentes con "nada"
                form_data = {k: v for k, v in form.cleaned_data.items() if v is not None and v != ''}
                final_data = base_data.copy()
                final_data.update(form_data)

                # Log de verificación de datos combinados
                logger.info(f"Formulario Tramite - Datos combinados para guardar/generar: {json.dumps(final_data, indent=2, ensure_ascii=False, default=str)}")

                # 3. Actualizar o crear Vehiculo y Persona con los datos combinados
                vehiculo = document.get_or_create_vehiculo()
                for field, value in final_data.items():
                    if hasattr(vehiculo, field):
                        setattr(vehiculo, field, value)
                vehiculo.save()

                propietario_nombre_completo = f"{final_data.get('propietario_primer_apellido', '')} {final_data.get('propietario_segundo_apellido', '')} {final_data.get('propietario_nombres', '')}".strip()
                propietario, created = Persona.objects.get_or_create(
                    numero_documento=final_data['propietario_documento'],
                    defaults={'nombre': propietario_nombre_completo}
                )
                propietario.nombre = propietario_nombre_completo
                propietario.direccion = final_data.get('propietario_direccion')
                propietario.ciudad = final_data.get('propietario_ciudad')
                propietario.telefono = final_data.get('propietario_telefono')
                propietario.save()

                # 4. Crear el formulario de trámite en la BD
                formulario = form.save(commit=False)
                formulario.id_vehiculo = vehiculo
                formulario.id_propietario = propietario
                # Actualizar el modelo del formulario con los datos combinados
                for field, value in final_data.items():
                    if hasattr(formulario, field):
                        setattr(formulario, field, value)
                formulario.save()

                # 5. Preparar datos para el PDF y generar
                pdf_data = final_data.copy()
                pdf_data['placa'] = vehiculo.placa  # Añadir la placa que no está en el form

                success = self._generate_pdf_document(document, 'formulario_tramite', pdf_data)

                
                if success:
                    messages.success(request, 'Formulario de trámite generado exitosamente.')
                    return redirect('forms_generation:download', form_id=success)
                else:
                    messages.error(request, 'Error al generar el PDF del formulario.')
                    
            except Exception as e:
                logger.error(f"Error procesando formulario de trámite: {str(e)}")
                messages.error(request, 'Error al procesar el formulario.')
        else:
            logger.error(f"Errores en el formulario de trámite: {form.errors.as_json()}")
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
                # Combinar los datos extraídos con los datos adicionales del formulario
                # Los datos adicionales tienen prioridad sobre los extraídos
                form_data = extracted_data.copy()
                form_data.update(additional_data)
                
                success = generator.generate_contrato_mandato(
                    form_data,  # Pasar todos los datos combinados
                    additional_data.get('mandante', {}),
                    additional_data.get('mandatario', {}),
                    file_path
                )
            elif form_type == 'contrato_compraventa':
                # Construir payload completo y llamar directamente al PDFFormFiller
                from services.PdfFormFiller import PDFFormFiller
                vehiculo = extracted_data.get('vehiculo', {})
                vendedor = additional_data.get('vendedor', {})
                comprador = additional_data.get('comprador', {})
                valor_venta = additional_data.get('valor_venta')
                forma_pago = additional_data.get('forma_pago')
                ciudad_contrato = additional_data.get('ciudad_contrato')
                fecha_contrato = additional_data.get('fecha_contrato')
                organismo_transito = additional_data.get('organismo_transito') or extracted_data.get('registro', {}).get('organismo_transito')

                form_data = {
                    'vehiculo': vehiculo,
                    'vendedor': vendedor,
                    'comprador': comprador,
                    'valor_venta': valor_venta,
                    'forma_pago': forma_pago,
                    'ciudad_contrato': ciudad_contrato,
                    'fecha_contrato': fecha_contrato,
                    'organismo_transito': organismo_transito,
                }

                filler = PDFFormFiller()
                success = filler.fill_pdf_form('contrato_compraventa', form_data, file_path)
            elif form_type == 'formulario_tramite':
                # Los datos completos vienen del formulario en additional_data
                logger.info(f"Datos del formulario para PDF: {additional_data}")
                success = generator.generate_formulario_tramite(additional_data, file_path)
            
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
                # Construir nombre: tipodedocumento_placa.pdf
                try:
                    # Tipo de documento legible
                    tipo_doc = slugify(generated_form.get_form_type_display()) or 'documento'
                except Exception:
                    tipo_doc = 'documento'

                # Extraer placa desde los datos estructurados del documento
                placa = 'sin_placa'
                try:
                    data = generated_form.document.get_structured_data()
                    veh = (data or {}).get('vehiculo', {}) or {}
                    raw_placa = (veh.get('placa') or '').strip()
                    if raw_placa:
                        # Normalizar placa: solo letras/números, mayúsculas
                        import re
                        placa_clean = re.sub(r'[^A-Za-z0-9]', '', raw_placa).upper()
                        if placa_clean:
                            placa = placa_clean
                except Exception:
                    pass

                filename = f"{tipo_doc}_{placa}.pdf"
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
        
        # ✅ AGREGAR INFORMACIÓN DE SUSCRIPCIÓN PARA BLOQUEO
        try:
            subscription = self.request.user.subscription
            context['subscription'] = subscription
            context['documents_used'] = subscription.documents_used
            context['documents_limit'] = subscription.get_documents_limit()
            context['documents_remaining'] = subscription.get_remaining_documents()
            context['can_upload'] = subscription.can_generate_document()
            context['plan_name'] = subscription.get_plan_display()
        except:
            context['subscription'] = None
            context['documents_used'] = 0
            context['documents_limit'] = 3
            context['documents_remaining'] = 3
            context['can_upload'] = True
            context['plan_name'] = 'Starter'
        
        return context

class DeleteGeneratedFormView(LoginRequiredMixin, View):
    """Elimina un registro de formulario generado y su archivo PDF asociado."""
    def post(self, request, form_id):
        try:
            generated_form = GeneratedForm.objects.get(id=form_id, user=request.user)

            # Eliminar archivo del sistema si existe
            if generated_form.generated_file and generated_form.generated_file.name:
                try:
                    file_path = generated_form.generated_file.path
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception as e:
                    logger.warning(f"No se pudo eliminar el archivo asociado (id={form_id}): {e}")

            generated_form.delete()
            messages.success(request, 'Documento eliminado del historial correctamente.')
        except GeneratedForm.DoesNotExist:
            messages.error(request, 'No se encontró el registro a eliminar.')
        except Exception as e:
            logger.error(f"Error eliminando formulario generado (id={form_id}): {e}")
            messages.error(request, 'Ocurrió un error al eliminar el registro.')

        return redirect('forms_generation:history')

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