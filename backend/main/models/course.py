from django.db import models

from .subcategory import Subcategory

class Course(models.Model) :
    course_id = models.CharField(primary_key=True, max_length=8)
    credit = models.IntegerField()
    course_name_th = models.CharField(max_length=200)
    course_name_en = models.CharField(max_length=200)
    
    subcategory_id = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.course_code} - {self.course_name}"