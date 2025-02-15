import uuid

from django.db import models

# Create your models here.

class User(models.Model) :
    
    class Role(models.TextChoices) :
        STUDENT = 'student'
        INSPECTOR = 'inspector'
    
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    student_code = models.CharField(max_length=10, null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=Role.choices
    )
    
    
class Curriculum(models.Model) :
    # auto generate uuid
    curriculum_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    curriculum_name = models.CharField(max_length=200)
    total_credit = models.IntegerField()
    
    # curriculum_year example 2565
    curriculum_year = models.IntegerField()
    
    
class Category(models.Model) :
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    category_name = models.CharField(max_length=200)
    category_min_credit = models.IntegerField()
    
    curriculum_id = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    
    
class Subcategory(models.Model) :
    subcategory_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    subcategory_name = models.CharField(max_length=200)
    subcateory_min_credit = models.IntegerField()
    
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    
class Course(models.Model) :
    course_id = models.CharField(primary_key=True, max_length=8)
    credit = models.IntegerField()
    course_name_th = models.CharField(max_length=200)
    course_name_en = models.CharField(max_length=200)
    
    subcategory_id = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.course_code} - {self.course_name}"
    
    
class Enrollment(models.Model) :
    
    class Semester(models.IntegerChoices) :
        FIRST = 1
        SECOND = 2
    
    enrollment_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    semester = models.IntegerField(choices=Semester.choices)
    year = models.IntegerField()
    grade = models.DecimalField(max_digits=3, decimal_places=2)
    
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)    
    
    
class CourserCurriculum(models.Model) :
    course_curriculum = models.UUIDField(primary_key=True, default=uuid.uuid4)
    
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    curriculum_id = models.ForeignKey(Curriculum, on_delete=models.CASCADE)