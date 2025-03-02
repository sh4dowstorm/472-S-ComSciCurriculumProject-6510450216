from rest_framework import serializers

from ...models import Enrollment

class StudyResultSerializer(serializers.Serializer) :
    studied_semester = serializers.IntegerField()
    studied_year = serializers.IntegerField()
    grade = serializers.DecimalField(max_digits=3, decimal_places=2)
    
    def to_representation(self, instance):
        if not isinstance(instance, Enrollment) :
            raise serializers.ValidationError('unexpected object type in StudyResultSerializer class')

        return {
            'studied_semester': instance.semester,
            'studied_year': instance.year,
            'grade': instance.grade,
        }