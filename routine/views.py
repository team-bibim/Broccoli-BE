from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

from Exer.models import Exercise
from routine.models import Routine
from routine.models import RoutineDetail
from routine.models import RoutineBox
from usebody.models import Usebody

from routine.serializers import RoutineSerializer
from routine.serializers import RoutinecheckSerializer
from routine.serializers import RoutineModifySerializer
from routine.serializers import RoutineDetailSerializer
from routine.serializers import RoutineBoxSerializer

from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404



#루틴 생성 5-1
class RoutineCreateAPIView(APIView):
    def post(self,request):
        routine_data = {
             'routine_name' : request.data.get('routine_name'),
             'routine_comment' : request.data.get('routine_comment'),
             'routine_day' : request.data.get('routine_day'),
             'owner_id' : request.data.get('owner_id'),
        }
        serializer = RoutineSerializer(data=routine_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors)

#내가 담은 루틴 리스트 조회 5-2
class RoutineBoxCheckAPIView(APIView):
    def get(self, request, pk):
        box = get_list_or_404(RoutineBox, user_id=pk)

        serializer = RoutineBoxSerializer(box, many=True)
        return Response(serializer.data)

#내가 담은 루틴 리스트에 추가 5-3
class RoutineBoxCreateAPIView(APIView):
    def post(self, request,pk):
        serializer = RoutineBoxSerializer(data=request.data)
        #pk를 user_id로 넣고 request로 받은건 routine_id만
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors)

#내가 담은 루틴 리스트에서 삭제 5-4
#class RoutineBoxDeleteAPIView(APIView):
 #   def delete(self,request,pk):



#루틴 조회 5-5
class RoutineCheckAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Routine, pk=pk)

    def get(self, request,pk):
        routine = self.get_object(pk)
        serializer = RoutinecheckSerializer(routine)
        return Response(serializer.data)

#루틴 수정 5-6
class RoutinePutAPIView(APIView):
    def get_object(self,pk):
        return get_object_or_404(Routine, pk=pk)

    def put(self,request, pk):
        routine = self.get_object(pk)
        serializer = RoutineModifySerializer(routine, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


#루틴 삭제 5-7
#루틴을 삭제할 때 루틴 세부 정보들도 함께 삭제해야 함
class RoutineDeleteAPIView(APIView):
    def get_object(self,pk):
        return get_object_or_404(Routine, pk=pk)

    def get_DetailObject(self, pk):
        return get_list_or_404(RoutineDetail, routine_id=pk)

    def delete(self, request, pk):
        routine = self.get_object(pk)
        routineDetail = self.get_DetailObject(pk)

        #루틴 정보 삭제
        routine.delete()

        #루틴 세부 정보들도 함께 삭제
        for obj in routineDetail:
            obj.delete()

        return Response(status=204)


#루틴 세부사항 생성 5-8
class RoutineDetailCreateAPIView(APIView):
    def post(self, request):
        # 전달되는 값들
        routineDetail_data = {
            'routine' : request.data.get('routine'),
            'exercise': request.data.get('exercise'),
            'usebody': request.data.get('usebody'),
            'day': request.data.get('day'),
        }
        serializer = RoutineDetailSerializer(data=routineDetail_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors)


#루틴 세부사항 조회 5-9
class RoutineDetailCheckAPIView(APIView):
    def get(self, request,pk):
        routineDetail = get_list_or_404(RoutineDetail, routine_id=pk)
        serializer = RoutineDetailSerializer(routineDetail, many=True)
        return Response(serializer.data)


#루틴 세부사항 수정 5-10
# class RoutineDetailPutAPIView(APIView):
#         #하루에 운동 하나? 여러개일 경우엔 뒤에 조건 하나 더
#         #객체 여러개일 때는 routineDetail.objects.filter
#
#     def put(self,request,pk):
#         get_object_or_404()
#         routineDetail = routineDetail.objects.filter(routine_id = pk)
#         serializer = RoutineDetailSerializer(routineDetail, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

# 처음부터 url에 루틴 id를 넘겨주고
# 수정 시 해당 루틴에 해당하는 상세사항들만 불러와서
# day 몇을 어떤 운동으로 수정할거냐? 같은 느낌
#
# day 몇에 있는 운동을 추가하거나 삭제하는 것.
# 그것이 생성 또는 삭제를 의미함.
#
# 삭제는 해당 루틴에 따른 운동을 모두 삭제한다.


#루틴 세부사항 삭제 5-11
class RoutineDetailDeleteAPIView(APIView):
    def delete(self, request,pk):
        routineDetail = get_object_or_404(RoutineDetail, pk= pk)
        routineDetail.delete()

        return Response(status=204)




