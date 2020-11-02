from django.urls import path

from . import views

urlpatterns = [
    path('bm/', views.before_match, name='before_match'),
]