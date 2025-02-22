from rest_framework import serializers

from ...models import Subcategory
from .course_serializer import CourseSerializer

class SubcategorySerializer(serializers.Serializer) :
    subcategory_name = serializers.CharField()
    min_credit = serializers.IntegerField()
    courses = serializers.SerializerMethodField()
    is_complete = serializers.BooleanField()
    
    def to_representation(self, instance):
        if not (instance.get('subcategory') and instance.get('courses') and isinstance(instance.get('isComplete'), bool)) :
            raise serializers.ValidationError('expected object with attribute name "subcategory" and "courses" and "isComplete" in SubcategorySerializer class')
        if not isinstance(instance['subcategory'], Subcategory) :
            raise serializers.ValidationError('unexpected object type in SubcategorySerializer class')
        
        return {
            'subcategory_name': instance['subcategory'].subcategory_name,
            'min_credit': instance['subcategory'].subcateory_min_credit,
            'courses': self.get_courses(instance['courses']),
            'is_complete': instance['isComplete'],
        }
        
    def get_courses(self, obj) :
        return CourseSerializer(obj, many=True).data