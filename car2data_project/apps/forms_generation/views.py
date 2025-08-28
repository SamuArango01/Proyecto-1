from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib import messages
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
        
        # Actualizar datos extraídos
        extracted_data, created = ExtractedData.objects.get_or_create(document=document)
        extracted_data.license_plate = request.POST.get('license_plate', '')
        extracted_data.vin = request.POST.get('vin', '')
        extracted_data.make = request.POST.get('make', '')
        extracted_data.model = request.POST.get('model', '')
        extracted_data.year = request.POST.get('year') or None
        extracted_data.owner_name = request.POST.get('owner_name', '')
        extracted_data.owner_address = request.POST.get('owner_address', '')
        extracted_data.owner_phone = request.POST.get('owner_phone', '')
        extracted_data.owner_email = request.POST.get('owner_email', '')
        extracted_data.save()
        
        return self.get(request, *args, **kwargs)

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