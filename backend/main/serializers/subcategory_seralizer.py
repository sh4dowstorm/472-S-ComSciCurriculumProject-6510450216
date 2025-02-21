from rest_framework import serializers

from ..models.subcategory import Subcategory

class SubcategorySerializer(serializers.ModelSeiralizer) :
    class Meta() :
        model = Subcategory
        fields = '__all__'