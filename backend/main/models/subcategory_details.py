import uuid
from django.db import models

from .credit_detail import CreditDetail
from .subcategory import Subcategory

class SubcategoryDetails(models.Model) :
    subcategory_detail_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    acquired_credit = models.IntegerField()
    
    subcateory_fk = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    credit_details_fk = models.ForeignKey(CreditDetail, on_delete=models.CASCADE)