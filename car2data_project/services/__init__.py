# Services package
# Services module for Car2Data project
"""
Módulo de servicios para Car2Data
Contiene servicios auxiliares como:
- PDFExtractor: Extracción de datos de PDFs usando Gemini AI
"""

from .pdf_extractor import PDFExtractor

__all__ = ['PDFExtractor']