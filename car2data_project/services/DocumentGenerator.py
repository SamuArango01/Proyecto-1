import os
import json
from datetime import datetime
from decimal import Decimal
from django.conf import settings
from django.template.loader import get_template
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
import logging

logger = logging.getLogger(__name__)

class DocumentGenerator:
    """
    Servicio para generar documentos PDF autodiligenciados
    """
    
    def __init__(self):
        self.templates_path = os.path.join(settings.BASE_DIR, 'templates', 'documents', 'pdf_templates')
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Configurar estilos personalizados para los PDFs"""
        if 'Title' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='Title',
                parent=self.styles['Heading1'],
                fontSize=16,
                spaceAfter=20,
                alignment=1,  # Centrado
                textColor=colors.HexColor('#0e2455')
            ))
        
        if 'Subtitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='Subtitle',
                parent=self.styles['Heading2'],
                fontSize=12,
                spaceAfter=12,
                textColor=colors.HexColor('#12c3d6')
            ))
        
        if 'Field' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='Field',
                parent=self.styles['Normal'],
                fontSize=10,
                spaceAfter=6,
            ))
    
    def generate_contrato_mandato(self, extracted_data, mandante_data, mandatario_data, document_path):
        """Genera un contrato de mandato autodiligenciado"""
        try:
            doc = SimpleDocTemplate(document_path, pagesize=letter)
            elements = []
            
            # Título
            title = Paragraph("CONTRATO DE MANDATO VEHICULAR", self.styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 20))
            
            # Debug: Log de los datos recibidos
            logger.info(f"Datos extraídos recibidos en generate_contrato_mandato: {extracted_data}")
            logger.info(f"Datos del mandante: {mandante_data}")
            logger.info(f"Datos del mandatario: {mandatario_data}")
            
            # Información del mandante
            mandante_section = Paragraph("DATOS DEL MANDANTE", self.styles['Subtitle'])
            elements.append(mandante_section)
            
            mandante_info = [
                ['Nombre:', mandante_data.get('nombre', 'N/A')],
                ['Documento:', mandante_data.get('documento', 'N/A')],
                ['Dirección:', mandante_data.get('direccion', 'N/A')],
                ['Teléfono:', mandante_data.get('telefono', 'N/A')],
                ['Ciudad:', mandante_data.get('ciudad', 'N/A')]
            ]
            
            mandante_table = Table(mandante_info, colWidths=[2*inch, 4*inch])
            mandante_table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
                ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ]))
            elements.append(mandante_table)
            elements.append(Spacer(1, 20))
            
            # Información del mandatario
            mandatario_section = Paragraph("DATOS DEL MANDATARIO", self.styles['Subtitle'])
            elements.append(mandatario_section)
            
            mandatario_info = [
                ['Nombre:', mandatario_data.get('nombre', 'N/A')],
                ['Documento:', mandatario_data.get('documento', 'N/A')],
                ['Dirección:', mandatario_data.get('direccion', 'N/A')],
                ['Teléfono:', mandatario_data.get('telefono', 'N/A')],
                ['Ciudad:', mandatario_data.get('ciudad', 'N/A')]
            ]
            
            mandatario_table = Table(mandatario_info, colWidths=[2*inch, 4*inch])
            mandatario_table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
                ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ]))
            elements.append(mandatario_table)
            elements.append(Spacer(1, 20))
            
            # Información del vehículo
            vehiculo_section = Paragraph("DATOS DEL VEHÍCULO", self.styles['Subtitle'])
            elements.append(vehiculo_section)
            
            # Asegurarse de que extracted_data es un diccionario
            if not isinstance(extracted_data, dict):
                logger.error(f"Error: extracted_data no es un diccionario: {type(extracted_data)}")
                extracted_data = {}
                
            # Obtener la información del vehículo de la estructura correcta
            vehiculo_info = extracted_data.get('vehiculo', {})
            logger.info(f"Información del vehículo extraída: {vehiculo_info}")
            
            vehiculo_data = [
                ['Placa:', vehiculo_info.get('placa', 'N/A')],
                ['Marca:', vehiculo_info.get('marca', 'N/A')],
                ['Línea:', vehiculo_info.get('linea', 'N/A')],
                ['Modelo:', str(vehiculo_info.get('modelo', 'N/A'))],
                ['Color:', vehiculo_info.get('color', 'N/A')],
                ['VIN:', vehiculo_info.get('vin', 'N/A')],
                ['Número de Motor:', vehiculo_info.get('numero_motor', 'N/A')],
                ['Número de Chasis:', vehiculo_info.get('numero_chasis', 'N/A')],
                ['Cilindrada (cc):', str(vehiculo_info.get('cilindrada_cc', 'N/A'))],
                ['Combustible:', vehiculo_info.get('combustible', 'N/A')],
                ['Servicio:', vehiculo_info.get('servicio', 'N/A')]
            ]
            
            vehiculo_table = Table(vehiculo_data, colWidths=[2*inch, 4*inch])
            vehiculo_table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
                ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ]))
            elements.append(vehiculo_table)
            elements.append(Spacer(1, 20))
            
            # Cláusulas del contrato
            clausulas_section = Paragraph("CLÁUSULAS", self.styles['Subtitle'])
            elements.append(clausulas_section)
            
            clausulas = [
                "PRIMERA: El MANDANTE confiere poder especial al MANDATARIO para realizar ante los organismos de tránsito todos los trámites relacionados con el vehículo descrito.",
                "SEGUNDA: El presente mandato incluye específicamente: Registro, matrícula, cambio de propietario, traspasos, y demás trámites ante autoridades de tránsito.",
                "TERCERA: El MANDATARIO se obliga a realizar las gestiones con la debida diligencia y cuidado.",
                "CUARTA: Este contrato se regirá por las leyes colombianas vigentes."
            ]
            
            for clausula in clausulas:
                elements.append(Paragraph(clausula, self.styles['Normal']))
                elements.append(Spacer(1, 12))
            
            # Firmas
            elements.append(Spacer(1, 40))
            firmas = [
                ['_________________________', '_________________________'],
                ['MANDANTE', 'MANDATARIO'],
                [mandante_data.get('nombre', 'N/A'), mandatario_data.get('nombre', 'N/A')],
                [f"C.C. {mandante_data.get('documento', 'N/A')}", f"C.C. {mandatario_data.get('documento', 'N/A')}"]
            ]
            
            firmas_table = Table(firmas, colWidths=[3*inch, 3*inch])
            firmas_table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ]))
            elements.append(firmas_table)
            
            # Fecha y ciudad
            fecha_info = f"Fecha: {datetime.now().strftime('%d de %B de %Y')}"
            elements.append(Spacer(1, 20))
            elements.append(Paragraph(fecha_info, self.styles['Normal']))
            
            doc.build(elements)
            logger.info(f"Contrato de mandato generado exitosamente: {document_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error generando contrato de mandato: {str(e)}")
            return False
    
    def generate_contrato_compraventa(self, extracted_data, vendedor_data, comprador_data, 
                                    valor_venta, document_path):
        """Genera un contrato de compraventa autodiligenciado"""
        try:
            doc = SimpleDocTemplate(document_path, pagesize=letter)
            elements = []
            
            # Título
            title = Paragraph("CONTRATO DE COMPRAVENTA VEHICULAR", self.styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 20))
            
            # Debug: Log de los datos recibidos
            logger.info(f"Datos extraídos recibidos en generate_contrato_compraventa: {extracted_data}")
            logger.info(f"Datos del vendedor: {vendedor_data}")
            logger.info(f"Datos del comprador: {comprador_data}")
            logger.info(f"Valor de venta: {valor_venta}")
            
            # Información del vendedor
            vendedor_section = Paragraph("DATOS DEL VENDEDOR", self.styles['Subtitle'])
            elements.append(vendedor_section)
            
            vendedor_info = [
                ['Nombre:', vendedor_data.get('nombre', 'N/A')],
                ['Documento:', vendedor_data.get('documento', 'N/A')],
                ['Dirección:', vendedor_data.get('direccion', 'N/A')],
                ['Teléfono:', vendedor_data.get('telefono', 'N/A')],
                ['Ciudad:', vendedor_data.get('ciudad', 'N/A')]
            ]
            
            vendedor_table = Table(vendedor_info, colWidths=[2*inch, 4*inch])
            vendedor_table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
                ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ]))
            elements.append(vendedor_table)
            elements.append(Spacer(1, 20))
            
            # Información del comprador
            comprador_section = Paragraph("DATOS DEL COMPRADOR", self.styles['Subtitle'])
            elements.append(comprador_section)
            
            comprador_info = [
                ['Nombre:', comprador_data.get('nombre', 'N/A')],
                ['Documento:', comprador_data.get('documento', 'N/A')],
                ['Dirección:', comprador_data.get('direccion', 'N/A')],
                ['Teléfono:', comprador_data.get('telefono', 'N/A')],
                ['Ciudad:', comprador_data.get('ciudad', 'N/A')]
            ]
            
            comprador_table = Table(comprador_info, colWidths=[2*inch, 4*inch])
            comprador_table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
                ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ]))
            elements.append(comprador_table)
            elements.append(Spacer(1, 20))
            
            # Información del vehículo
            vehiculo_section = Paragraph("DATOS DEL VEHÍCULO", self.styles['Subtitle'])
            elements.append(vehiculo_section)
            
            # Asegurarse de que extracted_data es un diccionario
            if not isinstance(extracted_data, dict):
                logger.error(f"Error: extracted_data no es un diccionario: {type(extracted_data)}")
                extracted_data = {}
                
            # Obtener la información del vehículo de la estructura correcta
            vehiculo_info = extracted_data.get('vehiculo', {})
            logger.info(f"Información del vehículo extraída: {vehiculo_info}")
            
            vehiculo_data = [
                ['Placa:', vehiculo_info.get('placa', 'N/A')],
                ['Marca:', vehiculo_info.get('marca', 'N/A')],
                ['Línea:', vehiculo_info.get('linea', 'N/A')],
                ['Modelo:', str(vehiculo_info.get('modelo', 'N/A'))],
                ['Color:', vehiculo_info.get('color', 'N/A')],
                ['VIN:', vehiculo_info.get('vin', 'N/A')],
                ['Número de Motor:', vehiculo_info.get('numero_motor', 'N/A')],
                ['Número de Chasis:', vehiculo_info.get('numero_chasis', 'N/A')],
                ['Cilindrada (cc):', str(vehiculo_info.get('cilindrada_cc', 'N/A'))],
                ['Combustible:', vehiculo_info.get('combustible', 'N/A')],
                ['Servicio:', vehiculo_info.get('servicio', 'N/A')],
                ['Clase de Vehículo:', vehiculo_info.get('clase_vehiculo', 'N/A')],
                ['Tipo de Carrocería:', vehiculo_info.get('tipo_carroceria', 'N/A')],
                ['Capacidad (Kg/PSJ):', str(vehiculo_info.get('capacidad_kg_psj', 'N/A'))],
                ['Potencia (HP):', str(vehiculo_info.get('potencia_hp', 'N/A'))],
                ['Puertas:', str(vehiculo_info.get('puertas', 'N/A'))]
            ]
            
            vehiculo_table = Table(vehiculo_data, colWidths=[2*inch, 4*inch])
            vehiculo_table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
                ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ]))
            elements.append(vehiculo_table)
            elements.append(Spacer(1, 20))
            
            # Valor de venta
            valor_section = Paragraph("VALOR DE LA VENTA", self.styles['Subtitle'])
            elements.append(valor_section)
            
            valor_formateado = f"${valor_venta:,.2f}" if valor_venta else "N/A"
            valor_info = [
                ['Valor en números:', valor_formateado],
                ['Valor en letras:', self.number_to_words(valor_venta) if valor_venta else 'N/A']
            ]
            
            valor_table = Table(valor_info, colWidths=[2*inch, 4*inch])
            valor_table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
                ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ]))
            elements.append(valor_table)
            elements.append(Spacer(1, 20))
            
            # Cláusulas del contrato
            clausulas_section = Paragraph("CLÁUSULAS", self.styles['Subtitle'])
            elements.append(clausulas_section)
            
            clausulas = [
                "PRIMERA: El VENDEDOR declara ser propietario del vehículo descrito y lo vende al COMPRADOR.",
                "SEGUNDA: El COMPRADOR acepta la compra del vehículo en las condiciones descritas.",
                "TERCERA: El precio de venta es el establecido y será pagado en la forma acordada.",
                "CUARTA: El vehículo se entrega en el estado en que se encuentra.",
                "QUINTA: Los gastos de traspaso corren por cuenta del COMPRADOR."
            ]
            
            for clausula in clausulas:
                elements.append(Paragraph(clausula, self.styles['Normal']))
                elements.append(Spacer(1, 12))
            
            # Firmas
            elements.append(Spacer(1, 40))
            firmas = [
                ['_________________________', '_________________________'],
                ['VENDEDOR', 'COMPRADOR'],
                [vendedor_data.get('nombre', 'N/A'), comprador_data.get('nombre', 'N/A')],
                [f"C.C. {vendedor_data.get('documento', 'N/A')}", f"C.C. {comprador_data.get('documento', 'N/A')}"]
            ]
            
            firmas_table = Table(firmas, colWidths=[3*inch, 3*inch])
            firmas_table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ]))
            elements.append(firmas_table)
            
            # Fecha y ciudad
            fecha_info = f"Fecha: {datetime.now().strftime('%d de %B de %Y')}"
            elements.append(Spacer(1, 20))
            elements.append(Paragraph(fecha_info, self.styles['Normal']))
            
            doc.build(elements)
            logger.info(f"Contrato de compraventa generado exitosamente: {document_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error generando contrato de compraventa: {str(e)}")
            return False
    
    def generate_formulario_tramite(self, extracted_data, documento_path):
        """Genera un formulario de trámite autodiligenciado"""
        try:
            doc = SimpleDocTemplate(documento_path, pagesize=letter)
            elements = []
            
            # Título
            title = Paragraph("FORMULARIO DE TRÁMITE VEHICULAR", self.styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 20))
            
            # Debug: Log de los datos recibidos
            logger.info(f"Datos extraídos recibidos en generate_formulario_tramite: {extracted_data}")
            
            # Información del vehículo
            vehiculo_section = Paragraph("INFORMACIÓN DEL VEHÍCULO", self.styles['Subtitle'])
            elements.append(vehiculo_section)
            
            # Asegurarse de que extracted_data es un diccionario
            if not isinstance(extracted_data, dict):
                logger.error(f"Error: extracted_data no es un diccionario: {type(extracted_data)}")
                extracted_data = {}
                
            # Obtener la información del vehículo y propietario de la estructura correcta
            vehiculo_info = extracted_data.get('vehiculo', {})
            propietario_info = extracted_data.get('propietario', {})
            
            logger.info(f"Información del vehículo extraída: {vehiculo_info}")
            logger.info(f"Información del propietario extraída: {propietario_info}")
            
            vehiculo_data = [
                ['Placa:', vehiculo_info.get('placa', 'N/A')],
                ['Marca:', vehiculo_info.get('marca', 'N/A')],
                ['Línea:', vehiculo_info.get('linea', 'N/A')],
                ['Modelo:', str(vehiculo_info.get('modelo', 'N/A'))],
                ['Color:', vehiculo_info.get('color', 'N/A')],
                ['VIN:', vehiculo_info.get('vin', 'N/A')],
                ['Número de Motor:', vehiculo_info.get('numero_motor', 'N/A')],
                ['Número de Chasis:', vehiculo_info.get('numero_chasis', 'N/A')],
                ['Cilindrada (cc):', str(vehiculo_info.get('cilindrada_cc', 'N/A'))],
                ['Combustible:', vehiculo_info.get('combustible', 'N/A')],
                ['Servicio:', vehiculo_info.get('servicio', 'N/A')],
                ['Clase de Vehículo:', vehiculo_info.get('clase_vehiculo', 'N/A')],
                ['Tipo de Carrocería:', vehiculo_info.get('tipo_carroceria', 'N/A')]
            ]
            
            vehiculo_table = Table(vehiculo_data, colWidths=[2*inch, 4*inch])
            vehiculo_table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
                ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
            ]))
            elements.append(vehiculo_table)
            elements.append(Spacer(1, 20))
            
            # Información del propietario
            propietario_section = Paragraph("INFORMACIÓN DEL PROPIETARIO", self.styles['Subtitle'])
            elements.append(propietario_section)
            
            # Usar propietario_info ya extraído
            propietario_data = [
                ['Nombre:', propietario_info.get('nombre', 'N/A')],
                ['Identificación:', propietario_info.get('identificacion', 'N/A')]
            ]
            
            propietario_table = Table(propietario_data, colWidths=[2*inch, 4*inch])
            propietario_table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
                ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
            ]))
            elements.append(propietario_table)
            elements.append(Spacer(1, 20))
            
            # Detalles de registro
            registro_section = Paragraph("DETALLES DE REGISTRO", self.styles['Subtitle'])
            elements.append(registro_section)
            
            registro_info = extracted_data.get('detalles_registro', {})
            registro_data = [
                ['Licencia de Tránsito:', registro_info.get('licencia_transito_numero', 'N/A')],
                ['Organismo de Tránsito:', registro_info.get('organismo_transito', 'N/A')],
                ['Fecha de Matrícula:', registro_info.get('fecha_matricula', 'N/A')],
                ['Fecha Expedición:', registro_info.get('fecha_expedicion_licencia', 'N/A')]
            ]
            
            registro_table = Table(registro_data, colWidths=[2*inch, 4*inch])
            registro_table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
                ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
            ]))
            elements.append(registro_table)
            elements.append(Spacer(1, 30))
            
            # Fecha y firma
            fecha_info = f"Fecha de diligenciamiento: {datetime.now().strftime('%d/%m/%Y')}"
            elements.append(Paragraph(fecha_info, self.styles['Normal']))
            elements.append(Spacer(1, 40))
            
            firma_info = "____________________________\nFirma del solicitante"
            elements.append(Paragraph(firma_info, self.styles['Normal']))
            
            doc.build(elements)
            logger.info(f"Formulario de trámite generado exitosamente: {documento_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error generando formulario de trámite: {str(e)}")
            return False
    
    def number_to_words(self, number):
        """Convierte números a palabras (implementación básica)"""
        try:
            # Implementación básica - en producción usar una librería como num2words
            if not number:
                return "Cero pesos"
            
            # Para simplificar, retornamos un formato básico
            return f"{number:.2f} pesos colombianos"
            
        except Exception:
            return "N/A"
    
    def get_document_path(self, form_type, document_id):
        """Genera la ruta donde se guardará el documento"""
        filename = f"{form_type}_{document_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        return os.path.join(settings.MEDIA_ROOT, 'generated_forms', filename)