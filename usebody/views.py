from rest_framework.response import Response
from rest_framework.views import APIView

from usebody.models import Usebody
from usebody.serializers import UsebodySerializer

from django.shortcuts import get_object_or_404

#04-01 운동 부위 조회
class UsebodyAPIView(APIView):
    def get(self, request):
        usebody = Usebody.objects.all()
        serializer = UsebodySerializer(usebody, many=True)
        return Response(serializer.data)

#04-02 운동 부위 상세정보 조회
class UsebodyDetailAPIView(APIView):
    #pk에 해당하는 객체 get
    def get_object(self, pk):
        return get_object_or_404(Usebody, pk=pk)

    def get(self, request, pk):
        usebody = self.get_object(pk)
        serializer = UsebodySerializer(usebody)
        return Response(serializer.data)