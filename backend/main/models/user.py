from django.db import models
import uuid

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
    