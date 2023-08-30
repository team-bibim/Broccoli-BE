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
    path('detail/delete/<int:pk>/', views.RoutineDetailDeleteAPIView.as_view()),

    path('box/<int:pk>/', views.RoutineBoxCreateAPIView.as_view()),
    path('box/check/<int:pk>/', views.RoutineBoxCheckAPIView.as_view()),
    path('box/delete/<int:pk>/', views.RoutineBoxDeleteAPIView.as_view()),

]