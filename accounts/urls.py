from django.urls import path
from .views import UserDetailAPI, RegisterUserAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-details/', UserDetailAPI.as_view()),
    path('register/', RegisterUserAPIView.as_view()),
]
