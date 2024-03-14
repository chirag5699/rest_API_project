from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    AuthUserRegistrationView,
    AuthUserLoginView,
    AuthUserListView,
    AuthUserUpdateView,
    AuthUserDeleteView
)

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', AuthUserRegistrationView.as_view(), name='user-register'),
    path('login/', AuthUserLoginView.as_view(), name='user-login'),
    path('update/', AuthUserUpdateView.as_view(), name='user-update'),
    path('delete/', AuthUserDeleteView.as_view(), name='user-delete'),
    path('', AuthUserListView.as_view(), name='user-list')

]