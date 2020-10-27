from django.urls import path, include
from . import views

urlpatterns = [
    path('match/', include('match.urls')),
]
