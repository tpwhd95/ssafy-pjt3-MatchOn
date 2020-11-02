from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# from .models import 

# 매칭 등록 시 
@api_view(['POST'])
def before_match(request):
    user = request.user
    data = request.data



    # return Response(UserSerializer(user).data, status=status.HTTP_200_OK)