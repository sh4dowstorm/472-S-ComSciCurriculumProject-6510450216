from typing import List
from rest_framework import serializers

from ...models import Course
from .study_result_serializer import StudyResultSerializer

class CourseSerializer(serializers.Serializer) :
    course_id = serializers.CharField()
    credit = serializers.IntegerField()
    results = serializers.SerializerMethodField()
    
    def to_representation(self, instance):
        if not (instance.get('data') and instance.get('result')) :
            raise serializers.ValidationError('expected object with attribute name "data" and "result" in CourseSerializer class')
        if not isinstance(instance['data'], Course) :
            raise serializers.ValidationError('unexpected object type in CourseSerializer class')
            
        return {
            'subcategory_name': instance['data'].course_id,
            'credit': instance['data'].credit,
            'result': self.get_results(instance['result']),
        }
        
    def get_results(self, studyResultSerialized) :
        return StudyResultSerializer(studyResultSerialized).data
        
    