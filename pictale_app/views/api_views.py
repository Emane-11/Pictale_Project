from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import DailyPhoto, Comment, Like, SavedPhoto, PhotoRecommendation
from ..serializers import (
    DailyPhotoSerializer, CommentSerializer, LikeSerializer, 
    SavedPhotoSerializer, PhotoRecommendationSerializer
)

# DailyPhoto API
class DailyPhotoViewSet(viewsets.ModelViewSet):
    queryset = DailyPhoto.objects.all().order_by('-date_featured')
    serializer_class = DailyPhotoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# Comment API
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

'''
like_photo / save_photo endpoints:

    Expect photo_id in the request body.

    Check if the user already liked/saved that photo.

    If yes → return a friendly message.

    If no → create the record and return it.
'''
# Like API
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def like_photo(self, request):
        user = request.user
        photo_id = request.data.get('photo_id')
        if not photo_id:
            return Response({"error": "photo_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the like already exists
        if Like.objects.filter(user=user, photo_id=photo_id).exists():
            return Response({"message": "You have already liked this photo."}, status=status.HTTP_200_OK)
        
        like = Like.objects.create(user=user, photo_id=photo_id)
        serializer = self.get_serializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# SavedPhoto API
class SavedPhotoViewSet(viewsets.ModelViewSet):
    queryset = SavedPhoto.objects.all()
    serializer_class = SavedPhotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def save_photo(self, request):
        user = request.user
        photo_id = request.data.get('photo_id')
        if not photo_id:
            return Response({"error": "photo_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the photo is already saved
        if SavedPhoto.objects.filter(user=user, photo_id=photo_id).exists():
            return Response({"message": "Photo already saved."}, status=status.HTTP_200_OK)
        
        saved = SavedPhoto.objects.create(user=user, photo_id=photo_id)
        serializer = self.get_serializer(saved)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# PhotoRecommendation API
class PhotoRecommendationViewSet(viewsets.ModelViewSet):
    queryset = PhotoRecommendation.objects.all().order_by('-created_at')
    serializer_class = PhotoRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]



# Permissions
from rest_framework import viewsets, permissions
from pictale_app.permissions import IsAuthorOrReadOnly

'''
   Any user can read all posts, comments, recommendations.

   Only the creator or an admin can edit or delete their objects.

   Prevents other users from changing content they do not own
   
'''
class DailyPhotoViewSet(viewsets.ModelViewSet):
    queryset = DailyPhoto.objects.all()
    serializer_class = DailyPhotoSerializer
    permission_classes = [IsAuthorOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

class PhotoRecommendationViewSet(viewsets.ModelViewSet):
    queryset = PhotoRecommendation.objects.all()
    serializer_class = PhotoRecommendationSerializer
    permission_classes = [IsAuthorOrReadOnly]



