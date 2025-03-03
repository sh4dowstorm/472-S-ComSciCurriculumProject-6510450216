from django.test import TestCase

from main.utils.mock_data import *
from main.services import OCRService
from django.conf import settings

class OCRResult(TestCase):
    def setUp(self):
        self.ocr = OCRService()
        self.grade_text = self.ocr.extract_text_from_pdf(settings.BASE_DIR/"main/utils/OCR_transcript_test.pdf")
        self.activity_text = self.ocr.extract_text_from_pdf(settings.BASE_DIR/"main/utils/activity_transcript_test.pdf")
        
    def test_ocr(self):
        print(self.grade_text)
        print("==============================================================")
        print(self.activity_text)
        
    def test_activity_status(self):
        print("activity status: ", self.ocr.get_activiy_status(self.activity_text, "6510450861"))
        
    def test_course_info(self):
        print(self.ocr.extract_course_info(self.grade_text))
    
    def test_student_info(self):
        print(self.ocr.get_student_info(self.grade_text))