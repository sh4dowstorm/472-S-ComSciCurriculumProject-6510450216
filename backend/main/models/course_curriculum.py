from django.db import models
import uuid

from .course import Course
from .curriculum import Curriculum

class CourseCurriculum(models.Model) :
    course_curriculum = models.UUIDField(primary_key=True, default=uuid.uuid4)
    
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    curriculum_id = models.ForeignKey(Curriculum, on_delete=models.CASCADE)