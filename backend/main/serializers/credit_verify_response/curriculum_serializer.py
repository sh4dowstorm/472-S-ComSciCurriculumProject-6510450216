from rest_framework import serializers

from ...models import Curriculum

class CurriculumSerializer(serializers.Serializer) :
    curriculum_name = serializers.CharField()
    total_credit = serializers.IntegerField()
    curriculum_year = serializers.IntegerField()
    
    def to_representation(self, instance):
        if not isinstance(instance, Curriculum) :
            raise serializers.ValidationError("mismatch type of Curriculum instance")
            
        return {
            'curriculum_name': instance.curriculum_name,
            'total_credit': instance.total_credit,
            'curriculum_year': instance.curriculum_year,
        }