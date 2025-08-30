from django.urls import path
from .views import frontend_views

urlpatterns = [
    path('', frontend_views.home, name="home"),
    path('comment/<int:photo_id>/', frontend_views.add_comment, name="add_comment"),
    path('like/<int:photo_id>/', frontend_views.like_photo, name="like_photo"),
    path('save/<int:photo_id>/', frontend_views.save_photo, name="save_photo"),
    
]
