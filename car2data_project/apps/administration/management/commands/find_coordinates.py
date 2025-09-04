# car2data_project/car2data_project/management/commands/find_coordinates.py

import os
from django.core.management.base import BaseCommand
from django.conf import settings
from services.CoordinateFinder import CoordinateFinder


class Command(BaseCommand):
    help = 'Herramienta para encontrar coordenadas exactas en PDFs oficiales'

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            type=str,
            choices=['grid', 'overlay', 'test'],
            help='Acción a realizar: grid (cuadrícula simple), overlay (cuadrícula sobre plantilla), test (probar coordenadas)'
        )
        parser.add_argument(
            '--template',
            type=str,
            choices=['formulario_tramite', 'contrato_compraventa', 'contrato_mandato'],
            help='Tipo de plantilla'
        )

    def handle(self, *args, **options):
        finder = CoordinateFinder()
        action = options['action']
        template = options.get('template')
        
        if action == 'grid':
            # Crear cuadrícula simple
            output_path = os.path.join(settings.MEDIA_ROOT, 'coordinate_grid.pdf')
            finder.create_coordinate_grid(output_path)
            self.stdout.write(
                self.style.SUCCESS(f'Cuadrícula creada en: {output_path}')
            )
            
        elif action == 'overlay':
            if not template:
                self.stdout.write(self.style.ERROR('Debes especificar --template'))
                return
                
            output_path = os.path.join(settings.MEDIA_ROOT, f'{template}_with_grid.pdf')
            try:
                finder.overlay_grid_on_template(template, output_path)
                self.stdout.write(
                    self.style.SUCCESS(f'Plantilla con cuadrícula creada en: {output_path}')
                )
            except FileNotFoundError as e:
                self.stdout.write(self.style.ERROR(str(e)))
                
        elif action == 'test':
            if not template:
                self.stdout.write(self.style.ERROR('Debes especificar --template'))
                return
            
            # Coordenadas de ejemplo para probar
            test_coordinates = {
                'formulario_tramite': {
                    'test_placa': (500, 750),
                    'test_marca': (150, 680),
                    'test_modelo': (500, 650),
                    'test_propietario': (120, 350),
                },
                'contrato_compraventa': {
                    'test_vendedor': (200, 720),
                    'test_comprador': (200, 600),
                    'test_vehiculo': (200, 480),
                    'test_precio': (200, 340),
                },
                'contrato_mandato': {
                    'test_mandante': (200, 680),
                    'test_mandatario': (200, 600),
                    'test_placa': (200, 480),
                    'test_fecha': (200, 380),
                }
            }
            
            coords = test_coordinates.get(template, {})
            output_path = os.path.join(settings.MEDIA_ROOT, f'{template}_test_coordinates.pdf')
            
            finder.create_test_overlay(template, coords, output_path)
            self.stdout.write(
                self.style.SUCCESS(f'Overlay de prueba creado en: {output_path}')
            )
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write('INSTRUCCIONES DE USO:')
        self.stdout.write('='*60)
        self.stdout.write('1. Abre el PDF generado junto con tu plantilla original')
        self.stdout.write('2. Identifica visualmente dónde están los campos que quieres llenar')
        self.stdout.write('3. Lee las coordenadas en la cuadrícula (X, Y desde abajo-izquierda)')
        self.stdout.write('4. Actualiza las coordenadas en services/PDFFormFiller.py')
        self.stdout.write('5. Usa "test" para verificar que las coordenadas son correctas')
        self.stdout.write('')
        self.stdout.write('Ejemplo de uso:')
        self.stdout.write('python manage.py find_coordinates overlay --template=formulario_tramite')
        self.stdout.write('python manage.py find_coordinates test --template=formulario_tramite')