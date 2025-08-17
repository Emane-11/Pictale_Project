from django.contrib import admin
from .models import DailyPhoto, Comment, Like, SavedPhoto, PhotoRecommendation

admin.site.register(DailyPhoto)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(SavedPhoto)
admin.site.register(PhotoRecommendation)
