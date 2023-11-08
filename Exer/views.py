from rest_framework.views import APIView
from rest_framework.response import Response

from Exer.models import Exercise
from usebody.models import Usebody
from Exer.serializers import ExerciseSerializer
from Exer.serializers import ExerciseDetailSerializer
from django.shortcuts import get_object_or_404

from django.db import connection

#03-01 부위별 운동 간단 조회
class ExerciseBodyAPIiew(APIView):
    def get_object(self,pk):
         return Exercise.objects.filter(usebody_id=pk)

    def get(self,request,pk):
        #pk를 usebody_id를 가지는 객체를 가져온다
        cursor = connection.cursor()
        sql = "select usebody_name from usebody where usebody_id = %s"
        cursor.execute(sql, [pk])
        result = cursor.fetchall()

        exercise = self.get_object(pk)
        serializer = ExerciseSerializer(exercise, many=True)

        for i in serializer.data:
            key = f'usebody_name'
            value= result[0][0]
            i[key] = value

        if not serializer.data:
            message = {
                "결과 없음"
            }
            return Response(message, status=404)
        return Response(serializer.data)


#03-02 운동 상세 조회
class ExerciseDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Exercise, pk=pk)

    def get(self, request,pk):
        exercise = list(Exercise.objects.filter(exercise_id = pk))

        body = []
        for i in exercise:
            u_id = i.usebody_id
            cursor = connection.cursor()
            sql = "select usebody_name from usebody where usebody_id = %s"
            cursor.execute(sql, [u_id])
            result = cursor.fetchall()
            body.append(result[0][0])

        serializer = ExerciseDetailSerializer(exercise, many=True)

        index = 0
        for i in serializer.data:
            key = f'usebody_name'
            value = body[index]
            i[key] = value
            index += 1

        if not serializer.data:
            message = {
                "결과 없음"
            }
            return Response(message, status=404)
        return Response(serializer.data)

#03-03 운동 검색
class ExerciseSearchAPIView(APIView):
    def post(self,request):
        body = []

        if not request.data.get('searchData') and not request.data.get('usebodyName'):
            objects = Exercise.objects.all()
            serializer = ExerciseDetailSerializer(objects, many=True)

            return Response(serializer.data)

        else:
            objectsKor = Exercise.objects.filter(exerciseName_English__icontains=request.data.get('searchData'))
            objectsEng = Exercise.objects.filter(exerciseName_Korean__icontains=request.data.get('searchData'))
            objectsEquip = Exercise.objects.filter(equipment_name__icontains=request.data.get('searchData'))
            combined_objects = list(objectsKor) + list(objectsEng) + list(objectsEquip)
            serializer = ExerciseDetailSerializer(combined_objects, many=True)

            if not request.data.get('usebodyName'):
                #searchdata만 고려해서 가져와

                if not serializer.data:
                    blank = {
                        "message": "검색 결과가 없습니다"
                    }
                    return Response(blank, status=404)
                else:
                    return Response(serializer.data)

            if not request.data.get('searchData'):
                #해당 부위와 일치하는 데이터만 가져와

                temp = Usebody.objects.filter(usebody_name = request.data.get('usebodyName'))

                #id 알아내기
                for i in temp:
                    bodyId = i.usebody_id

                body_filter = Exercise.objects.filter(usebody_id = bodyId)
                serializer = ExerciseDetailSerializer(body_filter, many=True)

                filtered_data = [item for item in serializer.data]


                if not filtered_data:
                    blank = {
                        "message": "검색 결과가 없습니다"
                    }
                    return Response(blank, status=404)
                else:
                    return Response(filtered_data)
            else:
                for i in combined_objects:
                    u_id = i.usebody_id

                    cursor = connection.cursor()
                    sql = "select usebody_name from usebody where usebody_id = %s"
                    cursor.execute(sql, [u_id])
                    result = cursor.fetchall()
                    body.append(result[0][0])


                index = 0
                for i in serializer.data:
                    key = f'usebody_name'
                    value = body[index]
                    i[key] = value
                    index += 1

                filtered_data = [item for item in serializer.data if
                                 item['usebody_name'] == request.data.get('usebodyName')]

                if not filtered_data:
                    blank = {
                        "message": "검색 결과가 없습니다"
                    }
                    return Response(blank, status=404)
                else:
                    return Response(filtered_data)