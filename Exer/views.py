from rest_framework.views import APIView
from rest_framework.response import Response

from Exer.models import Exercise
from Exer.serializers import ExerciseSerializer
from Exer.serializers import ExerciseDetailSerializer
from django.shortcuts import get_object_or_404


#03-01 부위별 운동 간단 조회
#usebody의 id 대신 name이 나오게 하려면 model을 수정해야 할 것으로 보임
class ExerciseBodyAPIiew(APIView):
    def get_object(self,pk):
         return Exercise.objects.filter(usebody_id=pk)

    def get(self,request,pk):
        exercise = self.get_object(pk)
        serializer = ExerciseSerializer(exercise)
        return Response(serializer.data)


#03-02 운동 상세 조회
class ExerciseDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Exercise, pk=pk)

    def get(self, request,pk):
        exercise = self.get_object(pk)
        serializer = ExerciseDetailSerializer(exercise)
        return Response(serializer.data)

#03-03 운동 검색
class ExerciseSearchAPIView(APIView):
    def post(self,request):
        data = request.data

        exercise = Exercise.objects.filter(exerciseName_Korean=data)
        serializer = ExerciseSerializer(exercise)

        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors)

