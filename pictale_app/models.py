from django.contrib.auth.models import AbstractUser
from django.db import models

# ----------------------------
# User Model
# ----------------------------
class User(AbstractUser):
    """
    Custom User model for the Pictale app.
    Inherits all default Django User fields and adds extra profile details.
    All the default fields needed come from AbstractUser:
    username, first_name, last_name, email, password, groups,
    user_permissions, is_active, is_superuser, is_staff, last_login, date_joined
    """
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        help_text="Optional profile picture for the user."
    )
    bio = models.TextField(
        blank=True,
        null=True,
        help_text="Short description about the user."
    )

    

    def __str__(self):
        return self.username

# ----------------------------
# Daily Photo Model
# ----------------------------
class DailyPhoto(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='daily_photos/')
    story = models.TextField()
    date_taken = models.DateField(blank=True, null=True)
    date_featured = models.DateField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='photos')

    def __str__(self):
        return self.title

# ----------------------------
# Comment Model
# ----------------------------
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(DailyPhoto, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

# ----------------------------
# Like Model
# ----------------------------
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(DailyPhoto, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

# ----------------------------
# Saved Photo Model
# ----------------------------
class SavedPhoto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_photos')
    post = models.ForeignKey(DailyPhoto, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} saved {self.post.title}"

# ----------------------------
# Photo Recommendation Model
# ----------------------------
class PhotoRecommendation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    title = models.CharField(max_length=255)
    story = models.TextField()
    image_file = models.ImageField(upload_to='recommendations/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Recommendation: {self.title} by {self.user.username}"