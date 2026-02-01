import os
import fitz  # PyMuPDF
import pdfplumber
from docx import Document
from typing import Optional
from loguru import logger

class ResumeParser:
    """Service for parsing resumes from PDF and DOCX formats."""
    
    @staticmethod
    def extract_text_from_pdf_pymupdf(file_path: str) -> str:
        """Extract text from PDF using PyMuPDF."""
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF with PyMuPDF: {e}")
            return ""
    
    @staticmethod
    def extract_text_from_pdf_pdfplumber(file_path: str) -> str:
        """Extract text from PDF using pdfplumber (fallback method)."""
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF with pdfplumber: {e}")
            return ""
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """Extract text from DOCX file."""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {e}")
            return ""
    
    @staticmethod
    def parse_resume(file_path: str, filename: str) -> Optional[str]:
        """
        Parse resume and extract text.
        
        Args:
            file_path: Path to the resume file
            filename: Name of the file
            
        Returns:
            Extracted text or None if extraction failed
        """
        file_extension = os.path.splitext(filename)[1].lower()
        
        text = ""
        
        if file_extension == ".pdf":
            # Try PyMuPDF first
            text = ResumeParser.extract_text_from_pdf_pymupdf(file_path)
            
            # If PyMuPDF fails, try pdfplumber
            if not text or len(text) < 50:
                logger.info("PyMuPDF extraction insufficient, trying pdfplumber...")
                text = ResumeParser.extract_text_from_pdf_pdfplumber(file_path)
        
        elif file_extension == ".docx":
            text = ResumeParser.extract_text_from_docx(file_path)
        
        else:
            logger.error(f"Unsupported file format: {file_extension}")
            return None
        
        if not text or len(text) < 50:
            logger.warning("Extracted text is too short or empty")
            return None
        
        return text
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize extracted text."""
        # Remove multiple spaces
        text = " ".join(text.split())
        
        # Remove multiple newlines
        text = "\n".join(line.strip() for line in text.split("\n") if line.strip())
        
        return text
