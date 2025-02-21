from rest_framework import serializers

from .subcategory_seralizer import SubcategorySerializer

class MappedSerializer(serializers.ModelSerializer) :
    subcategory = SubcategorySerializer()
    total_credit = serializers.SerializerMethodField()
    
    def get_total_creadit(self, obj) :
        if isinstance(obj.get('totalCredit'), int) :
            return obj.get('totalCredit')