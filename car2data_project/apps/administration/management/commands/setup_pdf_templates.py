# car2data_project/car2data_project/management/commands/setup_pdf_templates.py

import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Configura las plantillas PDF oficiales para el sistema de relleno de formularios'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source-dir',
            type=str,
            help='Directorio donde están ubicados los PDFs oficiales originales',
        )

    def handle(self, *args, **options):
        """Configurar plantillas PDF"""
        
        # Usar STATIC_ROOT para el directorio de plantillas
        pdf_templates_dir = os.path.join(settings.STATIC_ROOT, 'pdf_templates')
        
        # Crear directorio para plantillas PDF si no existe
        if not os.path.exists(pdf_templates_dir):
            os.makedirs(pdf_templates_dir, exist_ok=True)
            self.stdout.write(
                self.style.SUCCESS(f'Directorio creado: {pdf_templates_dir}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Directorio ya existe: {pdf_templates_dir}')
            )
        
        # Nombres esperados de las plantillas
        templates_info = {
            'formulario_tramite_template.pdf': {
                'description': 'Formulario oficial de trámite vehicular',
                'required': True
            },
            'contrato_compraventa_template.pdf': {
                'description': 'Contrato de compraventa vehicular',
                'required': True
            },
            'contrato_mandato_template.pdf': {
                'description': 'Contrato de mandato persona natural',
                'required': True
            },
        }
        
        # Verificar plantillas existentes
        self.stdout.write('\nVerificando plantillas existentes:')
        all_templates_ok = True
        
        for template_name, template_info in templates_info.items():
            template_path = os.path.join(pdf_templates_dir, template_name)
            if os.path.exists(template_path):
                self.stdout.write(
                    self.style.SUCCESS(f'✓ {template_name} - {template_info["description"]} (Ya existe)')
                )
            elif template_info['required']:
                self.stdout.write(
                    self.style.ERROR(f'✗ {template_name} - {template_info["description"]} (Faltante)')
                )
                all_templates_ok = False
        
        # Si se especifica un directorio fuente, intentar copiar los archivos faltantes
        source_dir = options.get('source_dir')
        if source_dir and os.path.exists(source_dir):
            self.stdout.write(f'\nCopiando plantillas desde: {source_dir}')
            
            for template_name, template_info in templates_info.items():
                template_path = os.path.join(pdf_templates_dir, template_name)
                if os.path.exists(template_path):
                    continue  # Saltar si ya existe
                    
                source_path = os.path.join(source_dir, template_name)
                if os.path.exists(source_path):
                    shutil.copy2(source_path, template_path)
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Copiado: {template_name}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ No encontrado: {source_path}')
                    )
        
        # Verificar qué plantillas están disponibles
        self.stdout.write('\n' + '='*60)
        self.stdout.write('ESTADO DE LAS PLANTILLAS PDF:')
        self.stdout.write('='*60)
        
        for template_name, description in templates_info.items():
            template_path = os.path.join(pdf_templates_dir, template_name)
            
            if os.path.exists(template_path):
                self.stdout.write(
                    self.style.SUCCESS(f'✓ {template_name} - DISPONIBLE')
                )
                self.stdout.write(f'  Descripción: {description}')
                self.stdout.write(f'  Ubicación: {template_path}')
            else:
                self.stdout.write(
                    self.style.ERROR(f'✗ {template_name} - FALTANTE')
                )
                self.stdout.write(f'  Descripción: {description}')
                self.stdout.write(f'  Se necesita en: {template_path}')
            
            self.stdout.write('')
        
        # Instrucciones para el usuario
        missing_templates = [name for name in templates_info.keys() 
                           if not os.path.exists(os.path.join(pdf_templates_dir, name))]
        
        if missing_templates:
            self.stdout.write(self.style.WARNING('\nINSTRUCCIONES:'))
            self.stdout.write('Para que el sistema de relleno de formularios funcione correctamente, necesitas:')
            self.stdout.write('')
            
            for i, template_name in enumerate(missing_templates, 1):
                self.stdout.write(f'{i}. Copia el PDF oficial "{template_name}" a:')
                self.stdout.write(f'   {os.path.join(pdf_templates_dir, template_name)}')
                self.stdout.write(f'   ({templates_info[template_name]})')
                self.stdout.write('')
            
            self.stdout.write('Los PDFs deben ser las plantillas oficiales en blanco (sin rellenar).')
            self.stdout.write('El sistema rellenará automáticamente estos formularios con los datos extraídos.')
            self.stdout.write('')
            self.stdout.write('Alternativamente, puedes usar:')
            self.stdout.write(f'python manage.py setup_pdf_templates --source-dir=/ruta/a/tus/pdfs')
        else:
            self.stdout.write(self.style.SUCCESS('\n¡PERFECTO! Todas las plantillas PDF están configuradas.'))
            self.stdout.write('El sistema puede ahora generar documentos oficiales usando las plantillas.')
        
        # Crear archivo .gitignore para el directorio de plantillas
        gitignore_path = os.path.join(pdf_templates_dir, '.gitignore')
        if not os.path.exists(gitignore_path):
            with open(gitignore_path, 'w') as f:
                f.write('# Mantener directorio pero ignorar plantillas PDF por copyright\n')
                f.write('*.pdf\n')
                f.write('!.gitkeep\n')
            
            # Crear .gitkeep
            gitkeep_path = os.path.join(pdf_templates_dir, '.gitkeep')
            with open(gitkeep_path, 'w') as f:
                f.write('')
                
            self.stdout.write(
                self.style.SUCCESS(f'Archivos de control Git creados en: {pdf_templates_dir}')
            )
        
        # Verificar dependencias
        try:
            from PyPDF2 import PdfReader, PdfWriter
            from reportlab.pdfgen import canvas
            self.stdout.write(self.style.SUCCESS('\n✓ Dependencias PyPDF2 y ReportLab disponibles'))
        except ImportError as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Error de dependencias: {e}'))
            self.stdout.write('Ejecuta: pip install PyPDF2 reportlab')
        
        self.stdout.write(
            self.style.SUCCESS('\n¡Configuración de plantillas PDF completada!')
        )