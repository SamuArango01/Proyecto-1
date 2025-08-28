import os
import base64
import json
import logging
from typing import Dict, List, Optional
import PyPDF2
import google.generativeai as genai
from django.conf import settings

logger = logging.getLogger(__name__)

class PDFExtractor:
    """
    Servicio para extraer información de PDFs usando la API de Gemini
    """
    
    def __init__(self):
        # Usar la configuración de Django
        self.api_key = getattr(settings, 'GEMINI_API_KEY', '')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY no está configurada en settings")
        
        # Configurar Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Prompt base para extracción de información vehicular
        self.base_prompt = """
        Eres un experto en análisis de documentos vehiculares. Tu tarea es extraer información específica de documentos PDF relacionados con vehículos.

        Por favor, extrae la siguiente información del documento y devuélvela en formato JSON:

        {
            "tipo_documento": "Tipo de documento (matrícula, SOAT, revisión técnico-mecánica, etc.)",
            "placa": "Número de placa del vehículo",
            "marca": "Marca del vehículo",
            "modelo": "Modelo del vehículo",
            "año": "Año del vehículo",
            "color": "Color del vehículo",
            "propietario": {
                "nombre": "Nombre completo del propietario",
                "identificacion": "Número de identificación",
                "direccion": "Dirección del propietario"
            },
            "fechas_importantes": {
                "fecha_emision": "Fecha de emisión del documento",
                "fecha_vencimiento": "Fecha de vencimiento (si aplica)"
            },
            "informacion_adicional": {
                "clase_vehiculo": "Clase de vehículo",
                "tipo_servicio": "Tipo de servicio",
                "cilindraje": "Cilindraje del motor",
                "capacidad": "Capacidad de pasajeros o carga"
            },
            "estado": "Estado del documento (vigente, vencido, etc.)",
            "observaciones": "Cualquier observación adicional relevante"
        }

        Si alguna información no está disponible en el documento, usa "No disponible" como valor.

        Documento a analizar:
        """
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extrae texto de un archivo PDF
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                
                return text.strip()
        except Exception as e:
            logger.error(f"Error al extraer texto del PDF {pdf_path}: {str(e)}")
            raise
    
    def encode_pdf_to_base64(self, pdf_path: str) -> str:
        """
        Codifica un PDF a base64 para enviarlo a Gemini
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_data = file.read()
                return base64.b64encode(pdf_data).decode('utf-8')
        except Exception as e:
            logger.error(f"Error al codificar PDF {pdf_path}: {str(e)}")
            raise
    
    def extract_vehicle_info(self, pdf_path: str) -> Dict:
        """
        Extrae información vehicular de un PDF usando Gemini
        """
        try:
            # Extraer texto del PDF primero (método más confiable)
            text = self.extract_text_from_pdf(pdf_path)
            
            # Crear prompt para análisis de texto
            text_prompt = self.base_prompt + f"\n\nTexto extraído del documento:\n{text}"
            
            # Generar respuesta con Gemini
            response = self.model.generate_content(text_prompt)
            
            # Intentar parsear la respuesta JSON
            try:
                response_text = response.text
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                
                if start_idx != -1 and end_idx != 0:
                    json_str = response_text[start_idx:end_idx]
                    extracted_data = json.loads(json_str)
                else:
                    # Si no se encuentra JSON, crear estructura básica
                    extracted_data = {
                        "tipo_documento": "No identificado",
                        "placa": "No disponible",
                        "marca": "No disponible",
                        "modelo": "No disponible",
                        "año": "No disponible",
                        "color": "No disponible",
                        "propietario": {
                            "nombre": "No disponible",
                            "identificacion": "No disponible",
                            "direccion": "No disponible"
                        },
                        "fechas_importantes": {
                            "fecha_emision": "No disponible",
                            "fecha_vencimiento": "No disponible"
                        },
                        "informacion_adicional": {
                            "clase_vehiculo": "No disponible",
                            "tipo_servicio": "No disponible",
                            "cilindraje": "No disponible",
                            "capacidad": "No disponible"
                        },
                        "estado": "No disponible",
                        "observaciones": response_text
                    }
                
                return extracted_data
                
            except json.JSONDecodeError as e:
                logger.warning(f"Error al parsear JSON de Gemini: {str(e)}")
                # Crear estructura básica con la respuesta como observaciones
                return {
                    "tipo_documento": "No identificado",
                    "placa": "No disponible",
                    "marca": "No disponible",
                    "modelo": "No disponible",
                    "año": "No disponible",
                    "color": "No disponible",
                    "propietario": {
                        "nombre": "No disponible",
                        "identificacion": "No disponible",
                        "direccion": "No disponible"
                    },
                    "fechas_importantes": {
                        "fecha_emision": "No disponible",
                        "fecha_vencimiento": "No disponible"
                    },
                    "informacion_adicional": {
                        "clase_vehiculo": "No disponible",
                        "tipo_servicio": "No disponible",
                        "cilindraje": "No disponible",
                        "capacidad": "No disponible"
                    },
                    "estado": "No disponible",
                    "observaciones": response.text
                }
                
        except Exception as e:
            logger.error(f"Error al extraer información del PDF {pdf_path}: {str(e)}")
            raise
    
    def extract_text_info(self, pdf_path: str) -> Dict:
        """
        Extrae información usando solo el texto del PDF (método alternativo)
        """
        try:
            # Extraer texto del PDF
            text = self.extract_text_from_pdf(pdf_path)
            
            # Crear prompt para análisis de texto
            text_prompt = self.base_prompt + f"\n\nTexto extraído del documento:\n{text}"
            
            # Generar respuesta con Gemini
            response = self.model.generate_content(text_prompt)
            
            # Intentar parsear la respuesta JSON
            try:
                response_text = response.text
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                
                if start_idx != -1 and end_idx != 0:
                    json_str = response_text[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    return {
                        "tipo_documento": "No identificado",
                        "texto_extraido": text[:500] + "..." if len(text) > 500 else text,
                        "observaciones": response_text
                    }
                    
            except json.JSONDecodeError:
                return {
                    "tipo_documento": "No identificado",
                    "texto_extraido": text[:500] + "..." if len(text) > 500 else text,
                    "observaciones": response.text
                }
                
        except Exception as e:
            logger.error(f"Error al extraer información de texto del PDF {pdf_path}: {str(e)}")
            raise
