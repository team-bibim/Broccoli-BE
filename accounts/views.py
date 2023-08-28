import jwt
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from accounts.models import User, Follow
from accounts.serializers import UserSerializer, FollowSerializer
from accounts.utils import login_check
from my_settings import SECRET_KEY


# 01-01 이메일 회원가입
class SigninAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # JWT 토큰
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "Signin Success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK
            )

            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)

            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthAPIView(APIView):
    # 01 token에 따른 user 정보 가져오기
    def get(self, request):
        try:
            access = request.COOKIES.get('access')
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # token이 만료되었을 때
        except(jwt.ExpiredSignatureError):
            data = {'refresh': request.COOKIES('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access', access)
                res.set_cookie('refresh', refresh)
                return res
            raise jwt.exceptions.InvalidTokenError
        # 사용 불가능한 토큰일 때
        except(jwt.exceptions.InvalidTokenError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 01-02 이메일 로그인
    def post(self, request):
        # user 인증
        print(request.data)

        user = authenticate(
            username=request.data.get("email"), password=request.data.get("password")
        )

        # 회원가입한 user일 경우
        if user is not None:
            serializer = UserSerializer(user)
            # JWT 토큰
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "Login Success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token
                    },
                },
                status=status.HTTP_200_OK
            )
            # JWT 토큰을 Cookie에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 01-03 이메일 로그아웃
    def delete(self, request):
        response = Response({
            "message": "Logout Success"
        }, status=status.HTTP_200_OK)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response


class FollowAPIView(APIView):
    # API 08-01 팔로잉 조회
    @login_check
    def get(self, request):
        user_id = request.user.id
        following = Follow.objects.filter(follower_id=user_id)
        serializer = FollowSerializer(following, many=True)
        return Response(serializer.data)

    # API 08-02, 08-03 팔로우, 언팔로우
    @login_check
    def post(self, request):
        print(request.user)
        following_id = request.data.get('following_id')
        print(following_id)
        user_following = get_object_or_404(User, id=following_id)

        print(user_following)

        if user_following == request.user:
            return Response({'message': "Can't Follow Self"}, status=status.HTTP_400_BAD_REQUEST)

        is_following = Follow.objects.filter(follower=request.user, following=user_following).exists()

        if is_following:
            # 팔로잉 중인 상태: unfollow
            follow = Follow.objects.get(follower=request.user, following=user_following)
            follow.delete()
            message = 'Unfollowed Successfully'
        else:
            # 팔로잉 되어 있지 않은 상태: follow
            Follow.objects.create(follower=request.user, following=user_following)
            message = 'Followed Successfully'

        return Response({'messages': message}, status=status.HTTP_200_OK)







