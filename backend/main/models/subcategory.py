from django.db import models
import uuid

from .category import Category

class Subcategory(models.Model) :
    subcategory_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    subcategory_name = models.CharField(max_length=200)
    subcateory_min_credit = models.IntegerField()
    
    category_fk = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'subcategory name {self.subcategory_name}'