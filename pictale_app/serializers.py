from rest_framework import serializers
from .models import DailyPhoto, Comment, Like, SavedPhoto, PhotoRecommendation
from django.utils import timezone

# Nested serializer for comments
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at']

# Nested serializer for likes
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']

# Main serializer for DailyPhoto with nested comments and likes
class DailyPhotoSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)  # show all comments for this photo
    likes = LikeSerializer(many=True, read_only=True)        # show all likes for this photo

    class Meta:
        model = DailyPhoto
        fields = [
            'id', 'title', 'image', 'story', 'date_taken', 
            'date_featured', 'comments', 'likes'
        ]

# Serializer for SavedPhotos
class SavedPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPhoto
        fields = '__all__'

# Serializer for PhotoRecommendation

'''
    When an admin updates status (Ex: from 'pending' → 'approved'), 
   the serializer detects the change.

   reviewed_at is automatically set to current datetime.

   The field remains read-only for API users, they cannot manually set it
 '''


class PhotoRecommendationSerializer(serializers.ModelSerializer):
    reviewed_at = serializers.DateTimeField(read_only=True) #This ensures that only backend logic (when an admin approves/rejects a recommendation) can set reviewed_at

    class Meta:
        model = PhotoRecommendation
        fields = '__all__'


    def update(self, instance, validated_data):
        # Check if status is being updated
        new_status = validated_data.get('status', instance.status)
        if instance.status != new_status:
            instance.reviewed_at = timezone.now()  # set reviewed_at to current time
        return super().update(instance, validated_data)

# Serializer for Profile Updates

from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
        read_only_fields = ["id", "username"]  # don’t allow username changes
