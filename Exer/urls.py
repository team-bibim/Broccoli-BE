from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExerciseSearchAPIView.as_view()),
    path('<int:pk>/', views.ExerciseDetailAPIView.as_view()),
    path('body/<int:pk>/', views.ExerciseBodyAPIiew.as_view()),
]