from rest_framework.response import Response
from rest_framework.views import APIView

from usebody.models import Usebody
from usebody.serializers import UsebodySerializer


#04-01 운동 부위 조회
class UsebodyAPIView(APIView):
    def get(self, request):
        usebody = Usebody.objects.all()
        serializer = UsebodySerializer(usebody, many=True)
        return Response(serializer.data)

