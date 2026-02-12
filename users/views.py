from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, login as django_login, logout as django_logout

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        django_login(request, user)
        return Response({'message': 'Logged in', 'role': user.role, 'username': user.username})
    return Response({'error': 'Invalid credentials'}, status=401)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    return Response({'username': request.user.username, 'role': request.user.role})

@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny]) 
def logout_view(request):
    django_logout(request)
    return Response({'message': 'Logged out'})
    django_logout(request)
    return Response({'message': 'Logged out'})
