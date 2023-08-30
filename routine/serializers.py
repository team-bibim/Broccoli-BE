from rest_framework import serializers
from .models import Routine
from .models import RoutineDetail

class RoutineModifySerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.routine_name = validated_data.get('routine_name', instance.routine_name)
        instance.routine_comment = validated_data.get('routine_comment', instance.routine_comment)
        instance.routine_day = validated_data.get('routine_day', instance.routine_day)

        instance.save()
        return instance
    class Meta:
        model= Routine
        fields = ['routine_name', 'routine_comment', 'routine_day']

class RoutinecheckSerializer(serializers.ModelSerializer):
    class Meta:
        model= Routine
        fields = ['routine_id', 'routine_name', 'routine_comment', 'recommend_count', 'routine_day', 'owner_id',
                  'created_at']

class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = ['routine_name', 'routine_comment', 'routine_day', 'owner_id']
class RoutineDetailSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     instance = RoutineDetail.objects.create(**validated_data)
    #     return instance

    def update(self, instance, validated_data):
         instance.exercise_id = validated_data.get(' ', instance.exercise_id)
         instance.usebody_id = validated_data.get(' ', instance.usebody_id)

    class Meta:
        model= RoutineDetail
        fields= ['routine', 'exercise', 'usebody', 'day']
        #뒤에 _id 안붙여도 되나?

class RoutineBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model= RoutineBox
        fields= ['user', 'routine']


        #request.user.id -> id 만 불러오고