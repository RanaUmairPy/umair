from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet

router = DefaultRouter()
router.register(r'register', CustomUserViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),  # /register/ for registration, /register/login/ for login
]