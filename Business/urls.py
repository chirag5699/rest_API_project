from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    BusinessViewSet, BusinessPhotoViewSet, BusinessVideoViewSet, BusinesspdfViewSet, BusinessShowViewSet,
    BusinessTrivialViewSet, TrivialQuestionViewSet, QuestionAnswerViewSet, UserTrivialScoreViewSet, UserPathViewSet,BusinessbineryViewSet
)

router = DefaultRouter()
router.register(r'main', BusinessViewSet, basename='business')
router.register(r'photo', BusinessPhotoViewSet, basename='businessphotos')
router.register(r'video', BusinessVideoViewSet, basename='businessvideos')
router.register(r'binery', BusinessbineryViewSet, basename='businessbinery')
router.register(r'pdf', BusinesspdfViewSet, basename='businessoffers')
router.register(r'show', BusinessShowViewSet, basename='businessshows')
router.register(r'trivial', BusinessTrivialViewSet, basename='businesstrivials')



urlpatterns = [
    path('', include(router.urls)),
]
