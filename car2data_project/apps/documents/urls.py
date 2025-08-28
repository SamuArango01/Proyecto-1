from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('upload/', views.DocumentUploadView.as_view(), name='upload'),
    path('preview/<int:pk>/', views.DataPreviewView.as_view(), name='data_preview'),
    path('history/', views.DocumentHistoryView.as_view(), name='history'),
    path('process/<int:pk>/', views.ProcessDocumentView.as_view(), name='process'),
    path('reprocess/<int:pk>/', views.reprocess_document, name='reprocess'),
    path('status/<int:pk>/', views.document_status, name='status'),
]