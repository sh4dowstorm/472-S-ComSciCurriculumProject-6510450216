import uuid
from django.db import models

from .user import User

class Form(models.Model) :
    
    class FormStatus(models.TextChoices) :
        DRAFT =  'draft'
        SUBMITTED = 'submitted'
        VERIFIED = 'verified'
        
    class FormType(models.TextChoices) :
        CHECK = 'credit check'
        VERIFY = 'graduated verify'
        
    form_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    form_status = models.CharField(max_length=10, choices=FormStatus.choices, default=FormStatus.DRAFT)
    form_type = models.CharField(max_length=20, choices=FormType.choices)
    
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
    