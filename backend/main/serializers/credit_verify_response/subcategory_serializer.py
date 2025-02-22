from rest_framework import serializers

from ...models import Subcategory
from .course_serializer import CourseSerializer

class SubcategorySerializer(serializers.Serializer) :
    subcategory_name = serializers.CharField()
    min_credit = serializers.IntegerField()
    courses = serializers.SerializerMethodField()
    
    def to_representation(self, instance):
        if not (instance.get('data') and instance.get('values')) :
            raise serializers.ValidationError('expected object with attribute name "data" and "values" in SubcategorySerializer class')
        if not isinstance(instance['data'], Subcategory) :
            raise serializers.ValidationError('unexpected object type in SubcategorySerializer class')
        
        return {
            'subcategory_name': instance['data'].subcategory_name,
            'min_credit': instance['data'].subcateory_min_credit,
            'courses': self.get_courses(instance['values']),
        }
        
    def get_courses(self, obj) :
        return CourseSerializer(obj, many=True).data