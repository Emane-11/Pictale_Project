from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import api_views
from .views.auth import RegisterAPIView, CustomObtainAuthToken, LogoutAPIView, ProfileAPIView

router = DefaultRouter()
router.register(r'dailyphotos', api_views.DailyPhotoViewSet)
router.register(r'comments', api_views.CommentViewSet)
router.register(r'likes', api_views.LikeViewSet)
router.register(r'savedphotos', api_views.SavedPhotoViewSet)
router.register(r'recommendations', api_views.PhotoRecommendationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/login/', CustomObtainAuthToken.as_view(), name='login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='logout'),
    path('auth/profile/', ProfileAPIView.as_view(), name='profile'),
]
