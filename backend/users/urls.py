from django.urls import path

from . import views

urlpatterns = [
    path('kakao', views.KakaoLogin.as_view()),
]