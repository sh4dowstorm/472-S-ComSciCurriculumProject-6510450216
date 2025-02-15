from django.test import TestCase

from main.models import Category, Curriculum, Subcategory, Course, CourseCurriculum

class CalculateTestCase(TestCase) :
    def setUp(self):
        self.cur1 = Curriculum.objects.create(
            curriculum_name=''
        )
        category1 = Category.objects.create(
            category_name=''
        )
        
        return super().setUp()
    