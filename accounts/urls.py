from django.urls import path, include

from accounts.views import SigninAPIView, AuthAPIView, FollowAPIView, UserinfoAPIView, UserDetailAPIView

urlpatterns = [
    # path('', include('dj_rest_auth.urls')),
    # path('signin/', include('dj_rest_auth.registration.urls')),
    path('signin/', SigninAPIView.as_view()),
    path('auth/', AuthAPIView.as_view()),
    path('follow/', FollowAPIView.as_view()),
    path('info/', UserinfoAPIView.as_view()),
    path('<int:pk>/', UserDetailAPIView.as_view()),
]