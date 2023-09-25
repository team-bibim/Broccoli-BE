from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from accounts import views
from accounts.views import SigninAPIView, AuthAPIView, FollowAPIView, UserinfoAPIView, UserDetailAPIView, GoogleLogin, \
    KakaoLogin

urlpatterns = [
    # path('', include('dj_rest_auth.urls')),
    # path('signin/', include('dj_rest_auth.registration.urls')),
    path('signin/', SigninAPIView.as_view()),
    path('auth/', AuthAPIView.as_view()),
    path('follow/', FollowAPIView.as_view()),
    path('info/', UserinfoAPIView.as_view()),
    path('<int:pk>/', UserDetailAPIView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('google/login', views.google_login),
    path('google/callback/', views.google_callback),
    path('google/login/finish/', GoogleLogin.as_view()),
    path('kakao/login/', views.kakao_login),
    path('kakao/callback/', views.kakao_callback),
    path('kakao/login/finish/', KakaoLogin.as_view()),
]