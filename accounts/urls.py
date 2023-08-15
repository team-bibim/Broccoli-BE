from django.urls import path, include

from accounts.views import SigninAPIView

urlpatterns = [
    # path('', include('dj_rest_auth.urls')),
    # path('signin/', include('dj_rest_auth.registration.urls')),
    path('signin/', SigninAPIView.as_view())
]