from rest_framework import serializers
from .models import Routine
from .models import RoutineDetail
from .models import RoutineBox
from accounts.utils import login_check
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
        fields = ['routine_id', 'routine_name', 'routine_comment', 'recommend_count', 'routine_day', 'nickname',
                  'created_at']


class RoutineCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Routine
        #exclude = ['routine_id']
        fields= '__all__'
    # #@login_check
    # def create(self, validated_data):
    #     routine = Routine.objects.create(**validated_data)
    #     return routine
class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = ['routine_name', 'routine_comment','routine_day', 'nickname']
class RoutineDetailSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     instance = RoutineDetail.objects.create(**validated_data)
    #     return instance

    class Meta:
        model= RoutineDetail
        fields= ['routine_detail_id', 'routine', 'day']

        #뒤에 _id 안붙여도 되나?

class RoutineDetailCreateSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.exercise_id = validated_data.get(' ', instance.exercise_id)
        instance.usebody_id = validated_data.get(' ', instance.usebody_id)
        instance.routine_id = validated_data.get(' ', instance.routine_id)
    class Meta:
        model = RoutineDetail
        fields= ['routine', 'exercise', 'usebody', 'day']

class RoutineBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model= RoutineBox
        fields= ['user', 'routine']

    def create(self, validated_data):
        user = validated_data['user']
        routine= validated_data['routine']

        if RoutineBox.objects.filter(user= user, routine=routine).exists():
            raise serializers.ValidationError("이미 존재하는 루틴입니다.")

        return RoutineBox.objects.create(**validated_data)

class RoutinePopRecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model= Routine
        fields= ['routine_id', 'routine_name', 'routine_comment', 'recommend_count', 'routine_day', 'nickname']


class RoutineSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model= Routine
        fields=['routine_id','routine_name', 'routine_comment', 'nickname', 'created_at']



