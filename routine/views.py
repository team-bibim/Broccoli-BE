from django.shortcuts import render

from accounts.utils import login_check
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

from Exer.models import Exercise
from routine.models import Routine
from routine.models import RoutineDetail
from routine.models import RoutineBox
from usebody.models import Usebody
from accounts.models import Follow

from routine.serializers import RoutineSerializer
from routine.serializers import RoutinecheckSerializer
from routine.serializers import RoutineModifySerializer
from routine.serializers import RoutineDetailSerializer
from routine.serializers import RoutineBoxSerializer
from routine.serializers import RoutinePopRecommendSerializer
from routine.serializers import RoutineSearchSerializer
from routine.serializers import RoutineDetailCreateSerializer

from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.http import JsonResponse
from django.db import connection



#루틴 생성 5-1
class RoutineCreateAPIView(APIView):
    def post(self,request):
        routine_data = {
             'routine_name' : request.data.get('routine_name'),
             'routine_comment' : request.data.get('routine_comment'),
            #임시
             'recommend_count' : request.data.get('recommend_count'),

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
    @login_check
    def get(self, request):
        box = get_list_or_404(RoutineBox, user_id=request.user.id)

        serializer = RoutineBoxSerializer(box, many=True)
        return Response(serializer.data)

#내가 담은 루틴 리스트에 추가 5-3
class RoutineBoxCreateAPIView(APIView):
    @login_check
    def post(self, request):
        # box_data = {
        #     'user_id': request.user.id,
        #     'routine': request.data.get('routine'),
        # }

        request.data['user'] = request.user.id
        serializer = RoutineBoxSerializer(data=request.data)


        #serializer = RoutineBoxSerializer(data=box_data)
        #pk를 user_id로 넣고 request로 받은건 routine_id만
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors)

#내가 담은 루틴 리스트에서 삭제 5-4
class RoutineBoxDeleteAPIView(APIView):
    @login_check
    def post(self,request):
        request.data['user'] = request.user.id

        f1 = request.data.get('user')
        f2 = request.data.get('routine')


        queryset = RoutineBox.objects.filter(user=f1, routine=f2)
        temp = queryset

        deleted_data = {
            'message': '삭제 완료',
            'deleted_data': temp
        }

        not_deleted= {
            'message' : '해당 루틴이 존재하지 않음'
        }

        if queryset.exists():
            queryset.delete()
            return Response(deleted_data, status=204)
        else:
            return Response(not_deleted, status=404)


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
    @login_check
    def post(self,request, pk):
        routine = get_object_or_404(Routine, pk=pk)

        serializer = RoutineModifySerializer(routine, data=request.data)

        fail = {
            "message": "수정 권한이 없습니다."
        }

        if serializer.is_valid():
            if request.user.id != routine.owner_id:
                return Response(fail, status=404)
            else:
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=400)


#루틴 삭제 5-7
#루틴을 삭제할 때 루틴 세부 정보들도 함께 삭제해야 함
class RoutineDeleteAPIView(APIView):
    @login_check
    def delete(self, request, pk):
        routine = get_object_or_404(Routine, pk=pk)
        routineDetail = RoutineDetail.objects.filter(routine_id=pk)

        if request.user.id == routine.owner_id:
            # 루틴 정보 삭제
            routine.delete()

            # 루틴 세부 정보들도 함께 삭제
            for obj in routineDetail:
                obj.delete()

            success= { "message": "삭제 성공" }
            return Response(success, status=204)
        else:
            fail = { "message": "삭제할 권한이 없습니다."}
            return Response(fail, status=404)

#루틴 세부사항 생성 5-8
class RoutineDetailCreateAPIView(APIView):
    @login_check
    def post(self, request):
        cursor = connection.cursor()
        sql = "select owner_id from routine where routine_id = %s"
        sql2 = "select usebody_id from exercise where exercise_id= %s"

        cursor.execute(sql, [request.data.get('routine')])
        result = cursor.fetchall()

        cursor.execute(sql2, [request.data.get('exercise')])
        u_id = cursor.fetchall()

        r = request.data.get('routine')
        e = request.data.get('exercise')
        d = request.data.get('day')

        routineDetail_data = {
            'routine' : r,
            'exercise': e,
            'usebody': u_id[0][0],
            'day': d,
        }

        if result[0][0] == request.user.id:
            if not RoutineDetail.objects.filter(exercise= e, routine = r, day = d):
                serializer = RoutineDetailCreateSerializer(data=routineDetail_data)

                if serializer.is_valid():
                    serializer.save()

                    return Response(serializer.data, status=201)
                return Response(serializer.errors)
            else:
                over = {"message": "완전히 중복된 일정입니다."}
                return Response(over, status = 404)
        else:
            NP= {
                "message": "생성할 권한이 없습니다."
            }
            return Response(NP, status=404)

#루틴 세부사항 조회 5-9
class RoutineDetailCheckAPIView(APIView):
    def get(self, request,pk):
        routineDetail = RoutineDetail.objects.filter(routine_id=pk)

        if routineDetail.exists() == False:
            fail = {
                "message": "루틴 세부 존재하지 않음"
            }
            return Response(fail , status = 404)
        else:
            r1, r2, r3 = '', '', ''

            for i in routineDetail:
                cursor = connection.cursor()
                sqlR = "select routine_name from routine where routine_id = %s"
                sqlU = "select usebody_name from usebody where usebody_id = %s"
                sqlE = "select exerciseName_english from exercise where exercise_id = %s"
                #한글 번역 너무 구려서 영어로 함

                cursor.execute(sqlR, [i.routine_id])
                r1 = (cursor.fetchall())[0][0]

                cursor.execute(sqlU, [i.usebody_id])
                r2 = (cursor.fetchall())[0][0]

                cursor.execute(sqlE, [i.exercise_id])
                r3 = (cursor.fetchall())[0][0]

            serializer = RoutineDetailSerializer(routineDetail, many=True)

            for i in serializer.data:
                key1 = f'routine_name'
                key2 = f'usebody_name'
                key3 = f'exercise_name'

                value1 = r1
                value2 = r2
                value3 = r3

                i[key1] = value1
                i[key2] = value2
                i[key3] = value3

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

#루틴 세부사항 삭제 5-11
class RoutineDetailDeleteAPIView(APIView):
    @login_check
    def post(self, request):
        routine_Detail = RoutineDetail.objects.filter(routine_detail_id= request.data.get('deleteData'))

        #어차피 하나만 검색됨
        for i in routine_Detail:
            r_id = i.routine_id

            cursor = connection.cursor()
            sql = "select owner_id from routine where routine_id = %s"
            cursor.execute(sql, [r_id])
            result = cursor.fetchall()

            o_id = result[0][0]

        if o_id == request.user.id:
            routine_Detail.delete()
            success = {
                "message": "삭제 성공"
            }
            return Response(success, status=204)
        else:
            fail = {
                "message": "삭제 권한 없음"
            }
            return Response(fail, status=404)

#06-01 루틴 추천(팔로잉 중인 유저)
class FollowRecommendAPIView(APIView):
    @login_check
    def get(self, request):
        user_id = request.user.id
        objects = get_list_or_404(Follow, follower_id = user_id)

        matching_ids = [obj.following_id for obj in objects]

        r_objects= []

        for i in matching_ids:
            r_objects += list(Routine.objects.filter(owner_id= i))

        serializer = RoutinecheckSerializer(r_objects, many=True)

        return Response(serializer.data)


#06-02 루틴 추천(인기순)
class PopularRecommendAPIView(APIView):
    def get(self, request):
        recom = Routine.objects.all().order_by('-recommend_count')

        serializer = RoutinePopRecommendSerializer(recom, many=True)

        return Response(serializer.data)

#07-01 루틴 검색
#routine_comment, routine_name, owner_id에 대해 검색
class RoutineSearchAPIView(APIView):
    def post(self, request):
        if request.body:
            # routine_name, comment, id 각각 검사 후 반환
            objectsName = Routine.objects.filter(routine_name__icontains=request.data.get('searchData'))
            objectsComment = Routine.objects.filter(routine_comment__icontains=request.data.get('searchData'))
            objectsId = Routine.objects.filter(owner_id__icontains=request.data.get('searchData'))

            combined_objects = list(objectsName)+ list(objectsComment) + list(objectsId)

            serializer = RoutineSearchSerializer(combined_objects, many=True)

            return Response(serializer.data)
        else:
            #검색에 아무것도 안 넣었을 경우 모든 루틴 반환
            objects = Routine.objects.all()
            serializer = RoutineSearchSerializer(objects, many=True)

            return Response(serializer.data)

        #각각 request 3개씩 해놓고 하는 방법
        # routineSearch_data = {
        #     'routine_name': request.data.get('routine_name'),
        #     'routine_comment': request.data.get('routine_comment'),
        #     'owner_id': request.data.get('owner_id'),
        # }
        #
        # if routineSearch_data['routine_name'] is not None:
        #     objects = Routine.objects.filter(routine_name = routineSearch_data['routine_name'])
        # else:
        #     objects = Routine.objects.all()
        #
        # if routineSearch_data['routine_comment'] is not None:
        #     objects2 = [item for item in objects if item.routine_comment == routineSearch_data['routine_comment']]
        # else:
        #     objects2 = objects
        #
        # if routineSearch_data['owner_id'] is not None:
        #     objects3 = [item for item in objects2 if item.owner_id == routineSearch_data['owner_id']]
        # else:
        #     objects3 = objects2
        #
        # serializer = RoutinecheckSerializer(objects3, many=True)
        #
        # #routine_name = routineSearch_data['routine_name']
        # #이런식으로 접근 할 것
        # #RoutineSearchSerializer(routineSearch_data, many=true)
        #
        # return Response(serializer.data)
