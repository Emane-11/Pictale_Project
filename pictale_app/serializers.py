from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import DailyPhoto, Comment, Like, SavedPhoto, PhotoRecommendation

User = get_user_model()

# ----------------------------
# Comment Serializer
# ----------------------------
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # display username instead of ID

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'comment_text', 'created_at']


# ----------------------------
# Like Serializer
# ----------------------------
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # display username instead of ID

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']


# ----------------------------
# DailyPhoto Serializer
# ----------------------------
class DailyPhotoSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)  # show all comments for this photo
    likes = LikeSerializer(many=True, read_only=True)        # show all likes for this photo
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = DailyPhoto
        fields = [
            'id', 'title', 'image', 'story', 'date_taken', 
            'date_featured', 'comments', 'likes', 'comments_count', 'likes_count'
        ]


# ----------------------------
# SavedPhoto Serializer
# ----------------------------
class SavedPhotoSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # always current logged-in user
    post_title = serializers.CharField(source='post.title', read_only=True)
    post_author = serializers.CharField(source='post.author.username', read_only=True)

    class Meta:
        model = SavedPhoto
        fields = ['id', 'user', 'post', 'post_title', 'post_author', 'saved_at']


# ----------------------------
# PhotoRecommendation Serializer
# ----------------------------
class PhotoRecommendationSerializer(serializers.ModelSerializer):
    reviewed_at = serializers.DateTimeField(read_only=True)  # set automatically on status change
    user = serializers.StringRelatedField(read_only=True)    # show username instead of ID

    class Meta:
        model = PhotoRecommendation
        fields = '__all__'

    def update(self, instance, validated_data):
        new_status = validated_data.get('status', instance.status)
        if instance.status != new_status:
            instance.reviewed_at = timezone.now()  # automatically update reviewed_at
        return super().update(instance, validated_data)


# ----------------------------
# Profile Serializer
# ----------------------------
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
        read_only_fields = ["id", "username"]  # don’t allow username changes
