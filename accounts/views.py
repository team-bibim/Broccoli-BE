import os

import jwt
import requests
import rest_framework_simplejwt.exceptions
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from json import JSONDecodeError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from accounts.models import User, Follow, Userinfo
from accounts.serializers import UserSerializer, FollowSerializer, UserinfoSerializer
from accounts.utils import login_check
from broccoli.settings import SECRET_KEY


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

    @login_check
    def delete(self, request):
        request.user.delete()
        return Response({'message': 'Delete Account Successfully'}, status=status.HTTP_200_OK)


class AuthAPIView(APIView):
    # 01 token에 따른 user 정보 가져오기
    # def get(self, request):
    #     try:
    #         access = request.COOKIES.get('access')
    #         payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
    #         pk = payload.get('user_id')
    #         user = get_object_or_404(User, pk=pk)
    #         serializer = UserSerializer(instance=user)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     # token이 만료되었을 때
    #     except jwt.exceptions.ExpiredSignatureError:
    #         data = {'refresh': request.COOKIES.get('refresh', None)}
    #         serializer = TokenRefreshSerializer(data=data)
    #         if serializer.is_valid(raise_exception=True):
    #             access = serializer.validated_data.get('access', None)
    #             refresh = serializer.validated_data.get('refresh', None)
    #             payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
    #             pk = payload.get('user_id')
    #             user = get_object_or_404(User, pk=pk)
    #             serializer = UserSerializer(instance=user)
    #             res = Response(serializer.data, status=status.HTTP_200_OK)
    #             res.set_cookie('access', access)
    #             res.set_cookie('refresh', refresh)
    #             return res
    #         raise jwt.exceptions.InvalidTokenError
    #     # 사용 불가능한 토큰일 때
    #     except jwt.exceptions.InvalidTokenError:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #     except User.DoesNotExist:
    #         return Response({"message": "No Such User"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            access = request.COOKIES.get('access')
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            res = Response(serializer.data, status=status.HTTP_200_OK)
            # res = Response(
            #     {
            #         "user": serializer.data,
            #         "message": "Token is vaild",
            #         "token": {
            #             "access": access,
            #             "refresh": request.COOKIES.get('refresh'),
            #         },
            #     },
            #     status=status.HTTP_200_OK
            # )
            res.set_cookie('access', access)
            res.set_cookie('refresh', request.COOKIES.get('refresh'))
            return res
        # access token이 만료되었을 때
        except jwt.exceptions.ExpiredSignatureError:
            try:
                data = {'refresh': request.COOKIES.get('refresh', None)}
                serializer = TokenRefreshSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    access = serializer.validated_data.get('access', None)
                    refresh = serializer.validated_data.get('refresh', None)
                    payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                    pk = payload.get('user_id')
                    user = get_object_or_404(User, pk=pk)
                    serializer = UserSerializer(instance=user)
                    res = Response(serializer.data, status=status.HTTP_200_OK)
                    res.set_cookie('access', access)
                    res.set_cookie('refresh', refresh)
                    return res
            except rest_framework_simplejwt.exceptions.TokenError:
                return Response({"message": "로그인이 만료되었습니다."}, status=status.HTTP_200_OK)

            raise jwt.exceptions.InvalidTokenError
        # 사용 불가능한 토큰일 때
        except jwt.exceptions.InvalidTokenError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "No Such User"}, status=status.HTTP_400_BAD_REQUEST)

    # 01-02 이메일 로그인
    def post(self, request):
        # user 인증
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
        following_id = request.data.get('following_id')
        user_following = get_object_or_404(User, id=following_id)

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


class UserinfoAPIView(APIView):
    # API 02-01 회원 정보 입력
    @login_check
    def post(self, request):
        # User의 userinfo가 존재하는 지 확인
        is_exist = Userinfo.objects.filter(user_id=request.user.id)
        if is_exist:
            return Response({'message': 'User already had Userinfo'}, status=status.HTTP_400_BAD_REQUEST)

        # user 설정
        request.data['user'] = request.user.id

        # bmi 계산
        weight = request.data.get('weight')
        height = request.data.get('height') * 0.01
        bmi = round(weight / (height * height), 2)
        request.data['bmi'] = bmi

        serializer = UserinfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # API 02-03 회원 정보 수정
    # PUT vs PATCH
    # PUT : 모든 속성 수정 / PATCH : 일부 속성 수정
    @login_check
    def put(self, request):
        # User의 userinfo가 존재하는 지 확인
        is_exist = Userinfo.objects.filter(user_id=request.user.id)
        if not is_exist:
            return Response({'message': 'No Userinfo'}, status=status.HTTP_400_BAD_REQUEST)

        request.data['user'] = request.user.id

        userinfo = Userinfo.objects.get(user_id=request.user.id)

        # bmi 계산
        weight = request.data.get('weight')
        height = request.data.get('height') * 0.01
        bmi = round(weight / (height * height), 2)
        request.data['bmi'] = bmi

        serializer = UserinfoSerializer(userinfo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 02-04 내 정보 조회
    @login_check
    def get(self, request):
        try:
            userinfo = Userinfo.objects.get(user_id=request.user.id)
            serializer = UserinfoSerializer(userinfo)
            return Response(serializer.data)
        except Userinfo.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class UserDetailAPIView(APIView):
    # user_id -> 해당 유저의 상세 정보 조회
    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    # API 02-02 회원 정보 조회
    def get(self, request, pk):
        userinfo = Userinfo.objects.get(user_id=pk)

        # 계정 비공개 일 경우
        if userinfo.acc_visibility == 0:
            return Response({'message': 'This account is Private account'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserinfoSerializer(userinfo)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 소셜 로그인
BASE_URL = 'http://localhost:8000/'
GOOGLE_CALLBACK_URL = BASE_URL + 'accounts/google/callback/'
state = os.environ.get('STATE')


# API 01-04 구글 로그인
def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = os.environ.get('SOCIAL_AUTH_GOOGLE_CLIENT_ID')
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URL}&scope={scope}")


def google_callback(request):
    client_id = os.environ.get('SOCIAL_AUTH_GOOGLE_CLIENT_ID')
    client_secret = os.environ.get('SOCIAL_AUTH_GOOGLE_SECRET')
    code = request.GET.get('code')

    # 받은 코드로 구글에 access token 요청
    token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URL}&state={state}")

    # json으로 변환 & 에러 부분 파싱
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    # error 발생 시 종료
    if error is not None:
        raise JSONDecodeError(error)

    # 성공 시 access token 가져오기
    access_token = token_req_json.get('access_token')

    # access token으로 email을 구글에 요청
    email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code

    # error 발생 시 400 에러
    if email_req_status != 200:
        return JsonResponse({'message': 'Failed to get email'}, status=status.HTTP_400_BAD_REQUEST)

    # 성공 시 email 가져오기
    email_req_json = email_req.json()
    email = email_req_json.get('email')


    # email, access token, code로 회원가입/로그인
    try:
        # 전달 받은 email로 등록된 유저가 있는지 탐색
        user = User.objects.get(email=email)

        # FK로 연결 되어 있는 socialaccount 테이블에서 해당 이메일의 유저가 있는지 확인
        # socialaccount table -> allauth 제공
        social_user = SocialAccount.objects.get(user=user)

        # 다른 SNS로 가입
        if social_user is None:
            return JsonResponse({'message': 'Email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)

        # 존재하지만 구글 계정이 아닌 경우, error
        if social_user.provider != 'google':
            return JsonResponse({'message': 'No matching social type'}, status=status.HTTP_400_BAD_REQUEST)

        # 이미 구글로 가입되어 있는 경우 -> 로그인 & 해당 유저의 jwt 발급
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code

        # 중간에 문제가 발생하면 error
        if accept_status != 200:
            return JsonResponse({"message": "Failed to Signin"}, status=accept_status)

        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)

    except User.DoesNotExist:
        # 가입이 되어있지 않은 상태 -> 회원가입 & 유저의 jwt 발급
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code

        # 중간에 문제가 발생하면 error
        if accept_status != 200:
            return JsonResponse({"message": "Failed to Signin"}, status=accept_status)

        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)

    except SocialAccount.DoesNotExist:
        # 일반 회원으로 가입된 email일 경우
        return JsonResponse({'message': 'Email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URL
    client_class = OAuth2Client


# API 01-05 카카오 로그인
KAKAO_CALLBACK_URI = BASE_URL + 'accounts/kakao/callback/'

def kakao_login(request):
    client_id = os.environ.get('SOCIAL_AUTH_KAKAO_CLIENT_ID')
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code&scope=account_email")

def kakao_callback(request):
    client_id = os.environ.get('SOCIAL_AUTH_KAKAO_CLIENT_ID')
    code = request.GET.get("code")
    redirect_uri = KAKAO_CALLBACK_URI

    # access token을 받는다
    token_req = requests.get(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    if error is not None:
        raise JSONDecodeError(error)

    access_token = token_req_json.get("access_token")

    # email 정보 불러오기
    profile_request = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
    profile_json = profile_request.json()
    kakao_account = profile_json.get('kakao_account')
    email = kakao_account.get('email', None)
    print(email)

    try:
        # 전달 받은 email로 등록된 유저가 있는지 탐색
        user = User.objects.get(email=email)

        # FK로 연결 되어 있는 socialaccount 테이블에서 해당 이메일의 유저가 있는지 확인
        # socialaccount table -> allauth 제공
        social_user = SocialAccount.objects.get(user=user)

        if social_user is None:
            return JsonResponse({'message': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)

        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}/accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code

        # error 발생
        if accept_status != 200:
            return JsonResponse({'message': 'Failed to login'}, status=status.HTTP_400_BAD_REQUEST)

        accept_json = accept.json()
        accept_json.pop('user', None)

        return JsonResponse(accept_json)

    except User.DoesNotExist:
        data = {'access_token': access_token, "code": code}
        accept = requests.post(f"{BASE_URL}/accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code

        if accept_status != 200:
            return JsonResponse({"message": "Failed to login", "code": accept_status}, status=status.HTTP_400_BAD_REQUEST)

        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)


    except SocialAccount.DoesNotExist:
        # 일반 회원으로 가입된 email일 경우
        return JsonResponse({'message': 'Email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)


class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI



# kakao 로그인 문제 발생
# 구글 로그인 할 때, nickname이 ''으로 자동 저장 -> 카카오도 마찬가지
# nickname unique=True 설정 때문에 중복 데이터 삽입 으로 인한 오류
# 소셜 로그인을 할 때, 임의의 nickname 값을 넣어 주어야 함
# 이걸 어떻게 해야 하는가...?
# -> user model nickname default 값을 random string으로 설정