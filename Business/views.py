from django.shortcuts import render

# Create your views here.
from .models import (
    Business, BusinessPhoto, BusinessVideo, Businesspdf, BusinessShow,
    BusinessTrivial, TrivialQuestion, QuestionAnswer, UserTrivialScore, UserPath
)
from .serializers import (
    BusinessSerializer, BusinessPhotoSerializer, BusinessVideoSerializer, BusinesspdfSerializer , 
    BusinessShowSerializer, BusinessTrivialSerializer, TrivialQuestionSerializer, QuestionAnswerSerializer,
    UserTrivialScoreSerializer, UserPathSerializer
)
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions
from rest_framework import viewsets
from django.conf import settings
from rest_framework.parsers import MultiPartParser, JSONParser

class OwnerManagerAuthenticationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        user_role = user.role
        if user and (user_role == settings.USER_ROLE_OWNER
                     or user_role == settings.USER_ROLE_MANAGER): # 1 is Owner role
            return True
        return False
    
class OwnerMediaManagerAuthenticationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        user_role = user.role
        if user and (user_role == settings.USER_ROLE_OWNER 
                     or user_role == settings.USER_ROLE_MEDIA_MANAGER
                      or user_role == settings.USER_ROLE_MANAGER ): # giving photo upload access to media_manger, manager, and ower
            return True
        return False


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [permissions.IsAuthenticated, OwnerManagerAuthenticationPermission]

    def perform_create(self, serializer):
        business = serializer.save()
        users = self.request.data.get('users', [])
        business.users.set(users)

    def perform_update(self, serializer):
        business = serializer.save()
        users = self.request.data.get('users', [])
        business.users.set(users)
    
    def get_queryset(self):
        # Override queryset to filter only businesses associated with the current user
        if self.request.user and not isinstance(self.request.user, AnonymousUser):
            user = self.request.user
            return Business.objects.filter(users=user)
        
        return Business.objects.none()

class BusinessPhotoViewSet(viewsets.ModelViewSet):
    queryset = BusinessPhoto.objects.all()
    serializer_class = BusinessPhotoSerializer
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [permissions.IsAuthenticated, OwnerMediaManagerAuthenticationPermission]
    

class BusinessVideoViewSet(viewsets.ModelViewSet):
    queryset = BusinessVideo.objects.all()
    serializer_class = BusinessVideoSerializer
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [permissions.IsAuthenticated, OwnerMediaManagerAuthenticationPermission]


class BusinesspdfViewSet(viewsets.ModelViewSet):
    queryset = Businesspdf.objects.all()
    serializer_class = BusinesspdfSerializer  
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [permissions.IsAuthenticated, OwnerMediaManagerAuthenticationPermission]


class BusinessShowViewSet(viewsets.ModelViewSet):
    queryset = BusinessShow.objects.all()
    serializer_class = BusinessShowSerializer
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [permissions.IsAuthenticated, OwnerMediaManagerAuthenticationPermission]


class BusinessTrivialViewSet(viewsets.ModelViewSet):
    queryset = BusinessTrivial.objects.prefetch_related('trivial_questions').all()
    serializer_class = BusinessTrivialSerializer
    permission_classes = [permissions.IsAuthenticated, OwnerManagerAuthenticationPermission]

class TrivialQuestionViewSet(viewsets.ModelViewSet):
    queryset = TrivialQuestion.objects.prefetch_related('question_answers').all()
    serializer_class = TrivialQuestionSerializer
    permission_classes = [permissions.IsAuthenticated, OwnerManagerAuthenticationPermission]

    def create(self, request, *args, **kwargs):
        request_answers = request.data.get('answers', [])
        request.data.pop('answers')
        print(request.data)
        if not request_answers:
            return Response({"error": "At least one correct answer is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not any(answer.get("is_correct", False) for answer in request_answers):
            return Response({'error': 'At least one correct answer must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        question_serializer = self.get_serializer(data=request.data)
        print("\n\n\nquestion_serializer", question_serializer)
        if question_serializer.is_valid():
            question = question_serializer.save()

            for request_answer in request_answers:
                request_answer["question"] = question.id
                answer_serializer = QuestionAnswerSerializer(data=request_answer)
                if answer_serializer.is_valid():
                    answer_serializer.save()
                else:
                    question.delete()
                    return Response(answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(question_serializer.data, status=status.HTTP_201_CREATED)
        return Response(question_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BusinessbineryViewSet(viewsets.ModelViewSet):
    pass


