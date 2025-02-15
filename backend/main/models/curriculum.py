from django.db import models
import uuid

class Curriculum(models.Model) :
    # auto generate uuid
    curriculum_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    curriculum_name = models.CharField(max_length=200)
    total_credit = models.IntegerField()
    
    # curriculum_year example 2565
    curriculum_year = models.IntegerField()
    