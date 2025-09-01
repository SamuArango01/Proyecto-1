# Crear este archivo: car2data_project/apps/documents/migrations/0003_add_document_methods.py

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_document_extracted_data_json_and_more'),
    ]

    operations = [
        # Esta migración no requiere cambios en la base de datos,
        # solo actualiza los métodos del modelo Document
    ]