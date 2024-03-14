from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
# from business.models import BusinessPhoto, BusinessVideo, BusinessOffer, BusinessShow
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from .serializers import (
    AuthUserRegistrationSerializer,
    AuthUserUpdateSerializer,
    AuthUserLoginSerializer,
    AuthUserListSerializer,
    AuthUserDeleteSerializer
)
from .models import User


class AuthUserRegistrationView(APIView):
    serializer_class = AuthUserRegistrationSerializer
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        role = data.get("role", 2)
        if role == 3 or role == 4:
            user = request.user 
            if not user or not user.is_authenticated or user.role != 1:
                return Response("Error : You don't have permission to access this resource.", status=status.HTTP_403_FORBIDDEN)
        
        serializer = AuthUserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            status_code = status.HTTP_201_CREATED
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }
            return Response(response, status=status_code)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthUserLoginView(APIView):
    serializer_class = AuthUserLoginSerializer
    permission_classes = (AllowAny,)
    global user_role
    user_role = User.role
    def post(self, request):
      
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=request.data.get("email"))
        if valid:
            if not user or not user.is_active:
                response = {
                    'success': False,
                    'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'User not found, or user is not an active user'
                }
                return Response(response, status.HTTP_403_FORBIDDEN)

            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'user': {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "role": user.role
                    },                    
                
                }
            }

            return Response(response, status=status_code)


class AuthUserListView(APIView):
    serializer_class = AuthUserListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user.role != 1:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            users = User.objects.all().filter(is_active=True)
            serializer = self.serializer_class(users, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched users',
                'users': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)



class AuthUserUpdateView(APIView):
    serializer_class = AuthUserUpdateSerializer
    permission_classes = (IsAuthenticated,)
    # authentication_classes = [TokenAuthentication]


    def put(self, request):
        user = request.user
        data = request.data
        # token = Token.objects.get(user=request.user)
        if data.get('email') is not None:
            user.email = data.get('email')

        if data.get('first_name') is not None:
            user.first_name = data.get('first_name')

        if data.get('last_name') is not None:
            user.last_name = data.get('last_name')

        if data.get('role') is not None:
            user.role = data.get('role')

        if data.get('date_joined') is not None:
            user.date_joined = data.get('date_joined')

        if data.get('is_active') is not None:
            user.is_active = data.get('is_active')

        if data.get('is_deleted') is not None:
            user.is_deleted = data.get('is_deleted')

        if data.get('password') is not None:
            password = data.get('password')
            user.set_password(password)

        user.save()
        serializer = self.serializer_class(user)
        return Response({'users': serializer.data}, status=status.HTTP_200_OK)


class AuthUserDeleteView(APIView):
    serializer_class = AuthUserDeleteSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        user = request.user
        if user is not None and user.is_active:
            user.is_active = False
            user.delete()
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully deleted user'

            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'success': False,
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Failed to delete user'
            
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

