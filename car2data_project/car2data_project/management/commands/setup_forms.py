# car2data_project/management/commands/setup_forms.py

import os
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Configura los directorios necesarios para la generación de formularios'

    def handle(self, *args, **options):
        """Configurar directorios y archivos necesarios"""
        
        # Crear directorio para formularios generados
        forms_dir = os.path.join(settings.MEDIA_ROOT, 'generated_forms')
        if not os.path.exists(forms_dir):
            os.makedirs(forms_dir)
            self.stdout.write(
                self.style.SUCCESS(f'Directorio creado: {forms_dir}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Directorio ya existe: {forms_dir}')
            )
        
        # Crear directorio para logs si no existe
        logs_dir = os.path.join(settings.BASE_DIR, 'logs')
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
            self.stdout.write(
                self.style.SUCCESS(f'Directorio de logs creado: {logs_dir}')
            )
        
        # Crear directorio para fuentes si no existe
        fonts_dir = os.path.join(settings.BASE_DIR, 'static', 'fonts')
        if not os.path.exists(fonts_dir):
            os.makedirs(fonts_dir)
            self.stdout.write(
                self.style.SUCCESS(f'Directorio de fuentes creado: {fonts_dir}')
            )
        
        # Verificar configuración de Gemini
        if not hasattr(settings, 'GEMINI_API_KEY') or not settings.GEMINI_API_KEY:
            self.stdout.write(
                self.style.WARNING(
                    'GEMINI_API_KEY no está configurada. '
                    'Configúrala en tu archivo de configuración para usar la extracción de datos.'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('GEMINI_API_KEY está configurada ✓')
            )
        
        # Crear archivo .gitignore para el directorio de medios si no existe
        gitignore_path = os.path.join(settings.MEDIA_ROOT, '.gitignore')
        if not os.path.exists(gitignore_path):
            with open(gitignore_path, 'w') as f:
                f.write('# Ignorar archivos generados pero mantener directorios\n')
                f.write('*.pdf\n')
                f.write('*.docx\n')
                f.write('!.gitkeep\n')
            self.stdout.write(
                self.style.SUCCESS(f'Archivo .gitignore creado: {gitignore_path}')
            )
        
        self.stdout.write(
            self.style.SUCCESS('\n¡Configuración completada! El sistema está listo para generar formularios.')
        )