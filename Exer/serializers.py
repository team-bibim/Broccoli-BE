from rest_framework import serializers
from .models import Exercise

class ExerciseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['exerciseName_English', 'exerciseName_Korean', 'equipment_name', 'videolink']

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['usebody_id', 'exerciseName_English', 'exerciseName_Korean']
