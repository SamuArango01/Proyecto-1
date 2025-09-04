import os
import threading
import traceback
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Document, ExtractedData
from .forms import DocumentUploadForm
from services.pdf_extractor import PDFExtractor
import logging

logger = logging.getLogger(__name__)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'documents/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_documents = Document.objects.filter(user=self.request.user)
        
        # Documentos recientes (últimos 5)
        context['recent_documents'] = user_documents.order_by('-uploaded_at')[:5]
        
        # Contadores
        context['total_documents'] = user_documents.count()
        context['processed_documents'] = user_documents.filter(status='completed').count()
        context['processing_documents'] = user_documents.filter(status__in=['pending', 'processing']).count()
        
        return context

class DocumentUploadView(LoginRequiredMixin, CreateView):
    model = Document
    form_class = DocumentUploadForm
    template_name = 'documents/upload.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        
        # Iniciar procesamiento en segundo plano
        if self.object.file:
            logger.info(f"Iniciando procesamiento para documento {self.object.id}")
            thread = threading.Thread(
                target=self.process_document_background,
                args=(self.object.id,)
            )
            thread.daemon = True
            thread.start()
        
        messages.success(self.request, 'Documento subido exitosamente. El procesamiento comenzará en breve.')
        return response
    
    def process_document_background(self, document_id):
        """Procesa el documento en segundo plano"""
        document = None
        try:
            logger.info(f"Iniciando procesamiento en segundo plano para documento {document_id}")
            
            document = Document.objects.get(id=document_id)
            document.status = 'processing'
            document.save()
            
            logger.info(f"Documento marcado como 'processing': {document.name}")
            
            # Verificar que el archivo existe
            if not document.file or not os.path.exists(document.file.path):
                raise FileNotFoundError(f"El archivo no existe: {document.file.path if document.file else 'None'}")
            
            # Obtener la ruta del archivo
            pdf_path = document.file.path
            logger.info(f"Ruta del PDF: {pdf_path}")
            
            # Crear extractor y probar conexión
            extractor = PDFExtractor()
            
            # Probar conexión antes de procesar
            if not extractor.test_connection():
                raise Exception("No se pudo establecer conexión con el servicio de IA")
            
            logger.info("Conexión con Gemini establecida correctamente")
            
            # Extraer información usando Gemini con timeout
            try:
                extracted_data = extractor.extract_vehicle_info(pdf_path)
                logger.info(f"Datos extraídos: {extracted_data}")
                
                # Guardar los datos extraídos
                document.set_extracted_data(extracted_data)
                
                # Actualizar el tipo de documento si se identificó
                if extracted_data.get('tipo_documento') and extracted_data.get('tipo_documento') != 'No identificado':
                    doc_type = extracted_data.get('tipo_documento', '').lower()
                    doc_type_mapping = {
                        'matrícula': 'registration',
                        'matricula': 'registration',
                        'registro': 'registration',
                        'propiedad': 'ownership',
                        'tarjeta': 'ownership'
                    }
                    
                    for key, value in doc_type_mapping.items():
                        if key in doc_type:
                            document.document_type = value
                            break
                
                document.status = 'completed'
                document.processed_at = timezone.now()
                document.error_message = ''
                logger.info(f"Documento procesado exitosamente: {document.name}")
                
            except Exception as e:
                logger.error(f"Error durante la extracción de datos: {str(e)}")
                logger.error(traceback.format_exc())
                document.status = 'error'
                document.error_message = f"Error al extraer datos: {str(e)}"
            
            document.save()
            
        except FileNotFoundError as e:
            logger.error(f"Error de archivo no encontrado: {str(e)}")
            if document:
                document.status = 'error'
                document.error_message = f"Archivo no encontrado: {str(e)}"
                document.save()
        except Exception as e:
            logger.error(f"Error al procesar documento: {str(e)}")
            logger.error(traceback.format_exc())
            
            if document:
                document.status = 'error'
                document.error_message = f"Error inesperado: {str(e)}"
                document.save()
                logger.info(f"Documento {document_id} marcado como error")

class DataPreviewView(LoginRequiredMixin, TemplateView):
    template_name = 'documents/data_preview.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doc_id = kwargs['pk']
        document = get_object_or_404(Document, id=doc_id, user=self.request.user)
        
        # Obtener datos extraídos
        extracted_data = document.get_extracted_data()
        
        context['document'] = document
        context['extracted_data'] = extracted_data
        return context

class DocumentHistoryView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'documents/history.html'
    context_object_name = 'documents'
    paginate_by = 10
    
    def get_queryset(self):
        return Document.objects.filter(
            user=self.request.user
        ).order_by('-uploaded_at')

class ProcessDocumentView(LoginRequiredMixin, TemplateView):
    template_name = 'documents/process.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doc_id = kwargs['pk']
        context['document'] = get_object_or_404(
            Document, id=doc_id, user=self.request.user
        )
        return context

@login_required
@require_POST
@csrf_exempt
def reprocess_document(request, pk):
    """Reprocesa un documento"""
    try:
        document = get_object_or_404(Document, id=pk, user=request.user)
        
        logger.info(f"Reprocessing document {pk}")
        
        # Reiniciar estado
        document.status = 'processing'
        document.extraction_error = None
        document.extracted_data_json = None
        document.save()
        
        # Procesar en segundo plano
        upload_view = DocumentUploadView()
        thread = threading.Thread(
            target=upload_view.process_document_background,
            args=(document.id,)
        )
        thread.daemon = True
        thread.start()
        
        return JsonResponse({'status': 'success', 'message': 'Reprocesamiento iniciado'})
    except Exception as e:
        logger.error(f"Error en reprocess_document: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
def document_status(request, pk):
    """Obtiene el estado actual de un documento"""
    try:
        document = get_object_or_404(Document, id=pk, user=request.user)
        return JsonResponse({
            'status': document.status,
            'processed_at': document.processed_at.isoformat() if document.processed_at else None,
            'error': document.extraction_error
        })
    except Exception as e:
        logger.error(f"Error en document_status: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)})