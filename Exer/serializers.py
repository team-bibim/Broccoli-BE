from rest_framework import serializers
from .models import Exercise
from usebody.models import Usebody

class BodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Usebody
        fields= '__all__'
class ExerciseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['usebody_id','exerciseName_English', 'exerciseName_Korean', 'equipment_name', 'videolink']

class ExerciseSerializer(serializers.ModelSerializer):
    #usebody_name = serializers.SerializerMethodField()

    # def get_usebody_name(self, obj):
    #     return obj.usebody_name
    class Meta:
        model = Exercise

        fields = ['usebody_id', 'exerciseName_English', 'exerciseName_Korean']
