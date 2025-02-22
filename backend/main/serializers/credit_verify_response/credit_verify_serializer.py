from rest_framework import serializers

from .category_serializer import CategorySerializer
from .curriculum_serializer import CurriculumSerializer

class CreditVerifySerializer(serializers.Serializer) :
    curriculum = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    
    def to_representation(self, instance):
        if not (instance.get('curriculum') and instance.get('categories')) :
            raise serializers.ValidationError('expect object with attribute name "curriculum" and "categories" in CreditVerifySerializer class')
        
        return {
            'curriculum': self.get_curriculum(instance['curriculum']),
            'categories': self.get_categories(instance['categories']),
        }
        
    def get_curriculum(self, obj) :
        return CurriculumSerializer(obj).data

    def get_categories(self, obj) :
        return CategorySerializer(obj, many=True).data