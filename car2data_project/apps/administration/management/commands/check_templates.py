import os
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Verifica las plantillas PDF del sistema'

    def handle(self, *args, **options):
        """Verificar plantillas PDF"""
        self.stdout.write("Verificando plantillas PDF...")
        
        # Directorio de plantillas
        templates_dir = os.path.join(settings.STATIC_ROOT, 'pdf_templates')
        self.stdout.write(f"Buscando plantillas en: {templates_dir}")
        
        # Verificar si el directorio existe
        if not os.path.exists(templates_dir):
            self.stdout.write(self.style.ERROR(f"El directorio no existe: {templates_dir}"))
            return
            
        # Listar archivos en el directorio
        try:
            files = os.listdir(templates_dir)
            self.stdout.write(self.style.SUCCESS("Archivos encontrados:"))
            for f in files:
                self.stdout.write(f"- {f}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al leer el directorio: {e}"))
