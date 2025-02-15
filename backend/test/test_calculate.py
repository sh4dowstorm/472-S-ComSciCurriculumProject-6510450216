from django.test import TestCase, RequestFactory

from main.models import Category, Curriculum, Subcategory, Course, Enrollment, User

class CalculateTestCase(TestCase) :
    def setUp(self):
        # setup user
        self.u = User.objects.create(
            email='abc@gmail.com',
            password='1234',
            name='doe',
            student_code='6510450569',
            role=User.Role.STUDENT,
        )
        
        # setup curriculum
        self.cur1 = Curriculum.objects.create(
            curriculum_name='หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาวิทยาการคอมพิวเตอร์',
            total_credit=124,
            curriculum_year=2565,
        )
        
        self.cate1 = Category.objects.create(
            category_name='หมวดวิชาศึกษาทั่วไป',
            category_min_credit=30,
            curriculum_id=self.cur1,
        )
        self.cate2 = Category.objects.create(
            category_name='หมวดวิชาเฉพาะ',
            category_min_credit=88,
            curriculum_id=self.cur1,
        )
        
        self.subcate1 = Subcategory.objects.create(
            subcategory_name='กลุ่มสาระภาษากับการสื่อสาร',
            subcateory_min_credit=13,
            category_id=self.cate1,
        )
        self.subcate2 = Subcategory.objects.create(
            subcategory_name='กลุ่มสาระอยู่ดีมีสุข',
            subcateory_min_credit=3,
            category_id=self.cate1,
        )
        self.subcate3 = Subcategory.objects.create(
            subcategory_name='วิชาแกน',
            subcateory_min_credit=12,
            category_id=self.cate2,
        )
        
        self.c1 = Course.objects.create(
            course_id='01175111-65',
            credit=1,
            course_name_th='กรีฑาลู่-ลาน เพื่อสุขภาพ',
            course_name_en='Track and Field for Health',
            subcategory_id=self.subcate2
        )
        self.c2 = Course.objects.create(
            course_id='01361101-65',
            credit=3,
            course_name_th='ภาษากับการสื่อสาร',
            course_name_en='English for Everyday Life',
            subcategory_id=self.subcate1
        )
        self.c3 = Course.objects.create(
            course_id='01417111-65',
            credit=3,
            course_name_th='แคลคูลัส',
            course_name_en='Calculus',
            subcategory_id=self.subcate3
        )
        
        # setup student enrollment
        self.st_enrollment = Enrollment.objects.create(
            semester=Enrollment.Semester.FIRST,
            year=2565,
            grade=3.50,
            user_id=self.u,
            course_id=self.c3,
        )
        
    def test_show(self) :
        print(self.u)
        print(self.cur1)
        print(self.cate1)
        print(self.cate2)
        print(self.subcate1)
        print(self.subcate2)
        print(self.subcate3)
        print(self.c1)
        print(self.c2)
        print(self.c3)
        print(self.st_enrollment)
    