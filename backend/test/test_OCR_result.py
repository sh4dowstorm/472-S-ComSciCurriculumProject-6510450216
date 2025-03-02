from django.test import TestCase

from main.utils.mock_data import *
from main.services import OCRService
from django.conf import settings

class OCRResult(TestCase) :
    def setUp(self) :
        self.ocr = OCRService()
        self.text = self.ocr.extract_text_from_pdf(settings.BASE_DIR/"main/utils/OCR_transcript_test.pdf")
        
    def test_ocr(self) :
        print(self.text)
        
    def test_course_info(self) :
        print(self.ocr.extract_course_info(self.text))
    
    def test_student_info(self) :
        print(self.ocr.get_student_info(self.text))