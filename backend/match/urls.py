from django.urls import path

from . import views

urlpatterns = [
    path('bm/', views.before_match, name='before_match'),
    path('match-room/', views.match_room, name='match_room'),
    path('am/', views.after_match, name='after_match'),
    path('result/', views.result, name='result'),
    path('report/', views.report, name='report'),
    path('report/<int:sports_pk>', views.report_detail, name='report_detail')
]