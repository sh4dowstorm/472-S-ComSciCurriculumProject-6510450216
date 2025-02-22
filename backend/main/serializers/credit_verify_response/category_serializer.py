from typing import List
from rest_framework import serializers

from ...models import Category, Course
from .subcategory_serializer import SubcategorySerializer
from .course_serializer import CourseSerializer

class CategorySerializer(serializers.Serializer) :
    category_name = serializers.CharField()
    min_credit = serializers.IntegerField()
    subcategories = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()
    
    def to_representation(self, instance):
        if not (instance.get('data') and instance.get('values') and isinstance(instance.get('isFreeElective'), bool)) :
            raise serializers.ValidationError('expected object with attribute name "data" and "values" and "isFreeElective" in CategorySerializer class')
        if not isinstance(instance['data'], Category) :
            raise serializers.ValidationError('unexpected object type in CategorySerializer class')

        if instance['isFreeElective'] :
            # incase of have no subcategory ex. หมวดวิชาเสรี
            return {
                'category_name': instance['data'].category_name,
                'min_credit': instance['data'].category_min_credit,
                'subcategories': None,
                'courses': self.get_courses(instance['values']),
            }
        
        return {
            'category_name': instance['data'].category_name,
            'min_credit': instance['data'].category_min_credit,
            'subcategories': self.get_subcategories(instance['values']),
            'courses': None,
        }
        
    def get_subcategories(self, obj) :
        return SubcategorySerializer(obj, many=True).data
    
    def get_courses(self, obj) :
        return CourseSerializer(obj, many=True).data