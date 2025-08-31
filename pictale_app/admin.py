from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, DailyPhoto, Comment, Like, SavedPhoto, PhotoRecommendation

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(DailyPhoto)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(SavedPhoto)
admin.site.register(PhotoRecommendation)
