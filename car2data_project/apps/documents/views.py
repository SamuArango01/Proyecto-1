import os
import threading
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

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'documents/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_documents'] = Document.objects.filter(
            user=self.request.user
        ).order_by('-uploaded_at')[:5]
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
        try:
            document = Document.objects.get(id=document_id)
            document.status = 'processing'
            document.save()
            
            # Obtener la ruta del archivo
            pdf_path = document.file.path
            
            # Extraer información usando Gemini
            extractor = PDFExtractor()
            extracted_data = extractor.extract_vehicle_info(pdf_path)
            
            # Guardar los datos extraídos
            document.set_extracted_data(extracted_data)
            
            # Actualizar el tipo de documento si se identificó
            if extracted_data.get('tipo_documento') != 'No identificado':
                doc_type_mapping = {
                    'matrícula': 'registration',
                    'registro': 'registration',
                    'SOAT': 'insurance',
                    'seguro': 'insurance',
                    'revisión': 'inspection',
                    'inspección': 'inspection',
                    'propiedad': 'ownership',
                    'tarjeta': 'ownership'
                }
                
                for key, value in doc_type_mapping.items():
                    if key.lower() in extracted_data.get('tipo_documento', '').lower():
                        document.document_type = value
                        break
            
            # Marcar como completado
            document.status = 'completed'
            document.processed_at = timezone.now()
            document.save()
            
        except Exception as e:
            # Marcar como error
            document = Document.objects.get(id=document_id)
            document.status = 'error'
            document.extraction_error = str(e)
            document.save()

class DataPreviewView(LoginRequiredMixin, TemplateView):
    template_name = 'documents/data_preview.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doc_id = kwargs['pk']  # Cambiado de 'doc_id' a 'pk'
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
        doc_id = kwargs['pk']  # Cambiado de 'doc_id' a 'pk'
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
        
        # Reiniciar estado
        document.status = 'processing'
        document.extraction_error = None
        document.save()
        
        # Procesar en segundo plano
        thread = threading.Thread(
            target=DocumentUploadView.process_document_background,
            args=(None, document.id)
        )
        thread.daemon = True
        thread.start()
        
        return JsonResponse({'status': 'success', 'message': 'Reprocesamiento iniciado'})
    except Exception as e:
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
        return JsonResponse({'status': 'error', 'message': str(e)})