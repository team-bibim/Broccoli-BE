from django.urls import path
from . import views

urlpatterns = [
    path('', views.RoutineCreateAPIView.as_view()),
    path('check/<int:pk>/', views.RoutineCheckAPIView.as_view()),
    path('modify/<int:pk>/', views.RoutinePutAPIView.as_view()),
    path('delete/<int:pk>/', views.RoutineDeleteAPIView.as_view()),

    path('detail/', views.RoutineDetailCreateAPIView.as_view()),
    path('detail/check/<int:pk>/', views.RoutineDetailCheckAPIView.as_view()),
    #path('detail/modify/<int:pk>/', views.RoutineDetailModifyAPIView.as_view()),
    path('detail/delete/', views.RoutineDetailDeleteAPIView.as_view()),

    path('box/', views.RoutineBoxCreateAPIView.as_view()),
    path('box/check/', views.RoutineBoxCheckAPIView.as_view()),
    path('box/delete/', views.RoutineBoxDeleteAPIView.as_view()),

    path('recommend/pop/', views.PopularRecommendAPIView.as_view()),
    path('recommend/follow/', views.FollowRecommendAPIView.as_view()),

    path('search/', views.RoutineSearchAPIView.as_view()),
]