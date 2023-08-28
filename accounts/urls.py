from django.urls import path, include

from accounts.views import SigninAPIView, AuthAPIView, FollowAPIView

urlpatterns = [
    # path('', include('dj_rest_auth.urls')),
    # path('signin/', include('dj_rest_auth.registration.urls')),
    path('signin/', SigninAPIView.as_view()),
    path('auth/', AuthAPIView.as_view()),
    path('follow/', FollowAPIView.as_view()),
]