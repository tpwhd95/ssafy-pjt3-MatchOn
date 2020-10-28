from django.urls import path, include
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('auth/', include('users.urls')),
    path('login/', obtain_jwt_token),
    path('match/', include('match.urls')),
]
