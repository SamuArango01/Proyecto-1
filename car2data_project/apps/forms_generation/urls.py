# car2data_project/apps/forms_generation/urls.py

from django.urls import path
from . import views

app_name = 'forms_generation'

urlpatterns = [
    # Vista principal de selección de formularios
    path('', views.FormSelectionView.as_view(), name='forms'),
    
    # Vista para generar formularios específicos
    path('generate/', views.GenerateFormView.as_view(), name='generate'),
    
    # Vista de descarga de formularios generados
    path('download/<int:form_id>/', views.DownloadFormView.as_view(), name='download'),
    
    # Vista para descargar PDF directamente
    path('download-pdf/<int:form_id>/', views.DownloadPDFView.as_view(), name='download_pdf'),
    
    # Vista del historial de formularios
    path('history/', views.FormHistoryView.as_view(), name='history'),
    
    # API para obtener datos de vista previa
    path('api/preview-data/', views.PreviewDataView.as_view(), name='preview_data'),
]