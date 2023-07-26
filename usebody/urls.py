from django.urls import path
from . import views

urlpatterns = [
    path('', views.UsebodyAPIView.as_view()),
]