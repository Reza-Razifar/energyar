from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from django.urls import path

urlpatterns = [
    path("login/", TokenObtainPairView.as_view()),
    path("login/refresh/", TokenRefreshView.as_view()),
]