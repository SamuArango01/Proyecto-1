from django.urls import path
from . import views

app_name = 'forms_generation'

urlpatterns = [
    path('', views.FormSelectionView.as_view(), name='forms'),
    path('generate/', views.GenerateFormView.as_view(), name='generate'),
    path('download/<int:form_id>/', views.DownloadFormView.as_view(), name='download'),
]