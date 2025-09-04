# car2data_project/services/CoordinateFinder.py

import os
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
import io

class CoordinateFinder:
    """
    Herramienta para encontrar las coordenadas exactas de campos en PDFs oficiales
    Genera un PDF con una cuadrícula para identificar posiciones exactas
    """
    
    def __init__(self):
        self.templates_path = os.path.join(settings.BASE_DIR, 'static', 'pdf_templates')
    
    def create_coordinate_grid(self, output_path):
        """
        Crea un PDF con cuadrícula y números para identificar coordenadas
        Usa tamaño extendido para cubrir formularios completos
        """
        packet = io.BytesIO()
        
        # Usar tamaño extendido para formularios oficiales
        extended_width = 650   # Más ancho que letter (612)
        extended_height = 850  # Más alto que letter (792)
        
        c = canvas.Canvas(packet, pagesize=(extended_width, extended_height))
        
        width, height = extended_width, extended_height
        
        # Configurar fuente
        c.setFont("Helvetica", 8)
        
        # Dibujar líneas verticales cada 50 puntos
        c.setStrokeColorRGB(0.7, 0.7, 0.7)  # Gris claro
        for x in range(0, int(width), 50):
            c.line(x, 0, x, height)
            # Números en la parte superior
            c.drawString(x + 2, height - 15, str(x))
        
        # Dibujar líneas horizontales cada 50 puntos
        for y in range(0, int(height), 50):
            c.line(0, y, width, y)
            # Números en el lado izquierdo
            c.drawString(5, y + 2, str(y))
        
        # Dibujar líneas más finas cada 10 puntos
        c.setStrokeColorRGB(0.9, 0.9, 0.9)  # Gris muy claro
        for x in range(0, int(width), 10):
            c.line(x, 0, x, height)
        for y in range(0, int(height), 10):
            c.line(0, y, width, y)
        
        # Agregar marcadores especiales en esquinas
        c.setFillColorRGB(1, 0, 0)  # Rojo
        c.setFont("Helvetica-Bold", 12)
        c.drawString(10, 10, "Origen (0,0)")
        c.drawString(10, height - 30, f"Superior Izq (0,{int(height)})")
        c.drawString(width - 120, 10, f"Inferior Der ({int(width)},0)")
        c.drawString(width - 150, height - 30, f"Superior Der ({int(width)},{int(height)})")
        
        # Agregar instrucciones
        c.setFillColorRGB(0, 0, 0)  # Negro
        c.setFont("Helvetica", 10)
        c.drawString(width/2 - 100, height - 50, "CUADRÍCULA DE COORDENADAS")
        c.drawString(width/2 - 150, height - 65, "Las coordenadas se miden desde ABAJO-IZQUIERDA (0,0)")
        c.drawString(width/2 - 120, height - 80, "Líneas gruesas cada 50 puntos, finas cada 10")
        
        c.save()
        packet.seek(0)
        
        # Guardar como archivo independiente
        with open(output_path, 'wb') as output_file:
            output_file.write(packet.getvalue())
        
        return packet
    
    def overlay_grid_on_template(self, template_type, output_path):
        """
        Superpone la cuadrícula sobre una plantilla específica
        Detecta automáticamente el tamaño de la plantilla
        """
        template_files = {
            'formulario_tramite': 'formulario_tramite_template.pdf',
            'contrato_compraventa': 'contrato_compraventa_template.pdf',
            'contrato_mandato': 'contrato_mandato_template.pdf',
        }
        
        template_file = template_files.get(template_type)
        if not template_file:
            raise ValueError(f"Tipo de plantilla no válido: {template_type}")
        
        template_path = os.path.join(self.templates_path, template_file)
        
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Plantilla no encontrada: {template_path}")
        
        # Leer la plantilla para detectar su tamaño
        from PyPDF2 import PdfReader
        template_pdf = PdfReader(template_path)
        
        if len(template_pdf.pages) == 0:
            raise ValueError("La plantilla no tiene páginas")
        
        # Obtener dimensiones de la primera página
        template_page = template_pdf.pages[0]
        mediabox = template_page.mediabox
        template_width = float(mediabox.width)
        template_height = float(mediabox.height)
        
        print(f"Dimensiones detectadas de la plantilla: {template_width} x {template_height} puntos")
        
        # Crear cuadrícula con las dimensiones exactas de la plantilla
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(template_width, template_height))
        
        # Configurar fuente
        c.setFont("Helvetica", 8)
        
        # Dibujar líneas verticales cada 50 puntos
        c.setStrokeColorRGB(0.7, 0.7, 0.7)  # Gris claro
        for x in range(0, int(template_width) + 50, 50):
            c.line(x, 0, x, template_height)
            # Números en la parte superior e inferior
            c.drawString(x + 2, template_height - 15, str(x))
            c.drawString(x + 2, 5, str(x))
        
        # Dibujar líneas horizontales cada 50 puntos
        for y in range(0, int(template_height) + 50, 50):
            c.line(0, y, template_width, y)
            # Números en ambos lados
            c.drawString(5, y + 2, str(y))
            c.drawString(template_width - 30, y + 2, str(y))
        
        # Dibujar líneas más finas cada 10 puntos
        c.setStrokeColorRGB(0.9, 0.9, 0.9)  # Gris muy claro
        for x in range(0, int(template_width) + 10, 10):
            c.line(x, 0, x, template_height)
        for y in range(0, int(template_height) + 10, 10):
            c.line(0, y, template_width, y)
        
        # Agregar marcadores especiales en esquinas
        c.setFillColorRGB(1, 0, 0)  # Rojo
        c.setFont("Helvetica-Bold", 10)
        c.drawString(10, 10, "Origen (0,0)")
        c.drawString(10, template_height - 30, f"Superior Izq (0,{int(template_height)})")
        c.drawString(template_width - 150, 10, f"Inferior Der ({int(template_width)},0)")
        c.drawString(template_width - 200, template_height - 30, f"Superior Der ({int(template_width)},{int(template_height)})")
        
        # Agregar instrucciones más visibles
        c.setFillColorRGB(0, 0, 0)  # Negro
        c.setFont("Helvetica-Bold", 12)
        c.drawString(template_width/2 - 120, template_height - 50, "CUADRÍCULA DE COORDENADAS")
        c.setFont("Helvetica", 10)
        c.drawString(template_width/2 - 180, template_height - 65, "Coordenadas desde ABAJO-IZQUIERDA (0,0)")
        c.drawString(template_width/2 - 140, template_height - 80, "Líneas gruesas cada 50 puntos, finas cada 10")
        c.drawString(template_width/2 - 100, template_height - 95, f"Tamaño: {int(template_width)} x {int(template_height)} puntos")
        
        c.save()
        packet.seek(0)
        
        # Crear cuadrícula como PDF independiente
        grid_pdf = PdfReader(packet)
        
        # Crear PDF de salida combinando plantilla + cuadrícula
        from PyPDF2 import PdfWriter
        output_pdf = PdfWriter()
        
        # Combinar primera página
        if len(template_pdf.pages) > 0:
            template_page = template_pdf.pages[0]
            grid_page = grid_pdf.pages[0]
            
            # Superponer cuadrícula sobre plantilla
            template_page.merge_page(grid_page)
            output_pdf.add_page(template_page)
        
        # Guardar resultado
        with open(output_path, 'wb') as output_file:
            output_pdf.write(output_file)
        
        print(f"Plantilla con cuadrícula guardada en: {output_path}")
        print(f"Dimensiones procesadas: {template_width} x {template_height} puntos")
        return True
    
    def create_test_overlay(self, template_type, coordinates_dict, output_path):
        """
        Crea un overlay de prueba para verificar coordenadas
        """
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=letter)
        c.setFont("Helvetica", 10)
        c.setFillColorRGB(1, 0, 0)  # Texto rojo para que se vea
        
        # Dibujar cada coordenada con su nombre
        for field_name, (x, y) in coordinates_dict.items():
            c.drawString(x, y, f"●{field_name}")
            # Dibujar un pequeño círculo
            c.circle(x, y, 3, stroke=1, fill=0)
        
        c.save()
        packet.seek(0)
        
        # Guardar overlay de prueba
        with open(output_path, 'wb') as output_file:
            output_file.write(packet.getvalue())
        
        return packet