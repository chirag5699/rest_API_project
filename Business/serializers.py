from rest_framework import serializers
from rest_framework.serializers import Serializer, FileField
from .models import (
    Business, BusinessPhoto, BusinessVideo, BusinessShow, Businesspdf,
    BusinessTrivial, TrivialQuestion, QuestionAnswer, UserTrivialScore, UserPath
)
from drf_extra_fields.fields import Base64ImageField, Base64FileField
from user.models import User
import filetype
from django.conf import settings

class Base64VideoFileField(Base64FileField):
    ALLOWED_TYPES = settings.SUPPORTED_VIDEO_TYPE
    def get_file_extension(self, filename, decoded_file):
        kind = filetype.guess(decoded_file)
        return kind.extension
   
    
class Base64ShowFileField(Base64FileField):
    ALLOWED_TYPES = settings.SUPPORTED_SHOW_TYPE
    def get_file_extension(self, filename, decoded_file):
        kind = filetype.guess(decoded_file)
        return kind.extension


class BusinessSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    logo = Base64ImageField(required=False)

    class Meta:
        model = Business
        fields = ['id', 'name', 'users', 'description', 'URL',
                  'phone', 'latitude', 'longitude', 'address', 'is_active', 'logo']
  
       
class BusinessPhotoSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False)

    class Meta:
        model = BusinessPhoto
        fields = '__all__'


class BusinessVideoSerializer(serializers.ModelSerializer):
    video = Base64VideoFileField(required=False)
    
    class Meta:
        model = BusinessVideo
        fields = '__all__'


class BusinesspdfSerializer(serializers.ModelSerializer):
    pdf = FileField()
    
    # class Meta:
    #     fields = ['file_uploaded']
    class Meta:
        model = Businesspdf
        fields = '__all__'


class BusinessShowSerializer(serializers.ModelSerializer):
    show = Base64ShowFileField(required=False)
    
    class Meta:
        model = BusinessShow
        fields = '__all__'





