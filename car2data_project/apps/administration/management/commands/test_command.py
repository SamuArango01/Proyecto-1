from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Comando de prueba para verificar la configuración de comandos personalizados'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('¡El comando de prueba se ejecutó correctamente!'))
