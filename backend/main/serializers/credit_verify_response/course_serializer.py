from typing import List
from rest_framework import serializers

from ...models import Course
from .study_result_serializer import StudyResultSerializer

class CourseSerializer(serializers.Serializer) :
    course_id = serializers.CharField()
    credit = serializers.IntegerField()
    results = serializers.SerializerMethodField()
    
    def to_representation(self, instance):
        if not (instance.get('course') and instance.get('studyResult')) :
            raise serializers.ValidationError('expected object with attribute name "course" and "studyResult" in CourseSerializer class')
        if not isinstance(instance['course'], Course) :
            raise serializers.ValidationError('unexpected object type in CourseSerializer class')
            
        return {
            'subcategory_name': instance['course'].course_id,
            'credit': instance['course'].credit,
            'results': self.get_results(instance['studyResult']),
        }
        
    def get_results(self, studyResultSerialized) :
        return StudyResultSerializer(studyResultSerialized).data
        
    