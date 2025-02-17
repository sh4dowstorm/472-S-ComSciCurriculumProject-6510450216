import uuid
from django.db import models

from .verification_result import VerificationResult

class CreditDetail(models.Model) :

    class CreditStatus(models.IntegerChoices) :
        COMPLETE = 1
        INCOMPLETE = 0

    credit_details_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    credit_status = models.IntegerField(choices=CreditStatus.choices, default=CreditStatus.INCOMPLETE)
    
    verification_result_id = models.ForeignKey(VerificationResult, on_delete=models.CASCADE)