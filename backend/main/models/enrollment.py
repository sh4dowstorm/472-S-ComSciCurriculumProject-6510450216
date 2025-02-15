from django.db import models
import uuid

from .user import User
from .course import Course

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
    
    def __str__(self):
        return f'course id {self.course_id.course_id}, ({self.semester, self.year}), {self.grade}'