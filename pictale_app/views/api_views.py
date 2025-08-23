from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import DailyPhoto, Comment, Like, SavedPhoto, PhotoRecommendation
from pictale_app.permissions import IsAuthorOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from ..serializers import (
    DailyPhotoSerializer, CommentSerializer, LikeSerializer, 
    SavedPhotoSerializer, PhotoRecommendationSerializer
)

# ----------------------------
# DailyPhoto API
# ----------------------------

class DailyPhotoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class DailyPhotoViewSet(viewsets.ModelViewSet):
    """
    CRUD for DailyPhoto.
    Anyone can read photos. Only authors or admins can update/delete.
    Logged-in users can create photos.
    """
    queryset = DailyPhoto.objects.all().order_by('-date_featured')
    serializer_class = DailyPhotoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = DailyPhotoPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['date_featured', 'author__username']  # exact match filters
    search_fields = ['title', 'story']  # partial match search

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ----------------------------
# Comment API
# ----------------------------
class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD for Comment.
    Anyone can read comments.
    Only authors or admins can update/delete.
    Logged-in users can create comments. Automatically assigns request.user as author.
    Supports filtering by photo via ?post_id=<id>
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.all().order_by('-created_at')
        post_id = self.request.query_params.get('post_id')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ----------------------------
# Like API
# ----------------------------
class LikeViewSet(viewsets.ModelViewSet):
    """
    CRUD for Like.
    Only authenticated users can create likes.
    Prevents duplicate likes.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def like_photo(self, request):
        user = request.user
        photo_id = request.data.get('photo_id')
        if not photo_id:
            return Response({"error": "photo_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate photo exists
        photo = get_object_or_404(DailyPhoto, id=photo_id)

        # Check if the like already exists
        if Like.objects.filter(user=user, post=photo).exists():
            return Response({"message": "You have already liked this photo."}, status=status.HTTP_200_OK)

        like = Like.objects.create(user=user, post=photo)
        serializer = self.get_serializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ----------------------------
# SavedPhoto API
# ----------------------------
class SavedPhotoViewSet(viewsets.ModelViewSet):
    """
    CRUD for SavedPhoto.
    Only authenticated users can save photos.
    Prevents duplicate saves.
    """
    queryset = SavedPhoto.objects.all()
    serializer_class = SavedPhotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def save_photo(self, request):
        user = request.user
        photo_id = request.data.get('photo_id')
        if not photo_id:
            return Response({"error": "photo_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate photo exists
        photo = get_object_or_404(DailyPhoto, id=photo_id)

        # Check if already saved
        if SavedPhoto.objects.filter(user=user, post=photo).exists():
            return Response({"message": "Photo already saved."}, status=status.HTTP_200_OK)

        saved = SavedPhoto.objects.create(user=user, post=photo)
        serializer = self.get_serializer(saved)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ----------------------------
# PhotoRecommendation API
# ----------------------------
class PhotoRecommendationViewSet(viewsets.ModelViewSet):
    """
    CRUD for PhotoRecommendation.
    Only authenticated users can create recommendations.
    Only admins can update the status (approved/rejected) and set reviewed_at.
    """
    queryset = PhotoRecommendation.objects.all().order_by('-created_at')
    serializer_class = PhotoRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        # Restrict status updates to admin users
        if not request.user.is_staff:
            return Response({"detail": "Only admins can update recommendations."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)



 
