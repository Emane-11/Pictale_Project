from django.urls import path
from .views import frontend_views

urlpatterns = [
    # Home + Photo actions
    path('', frontend_views.home, name="home"),
    path('comment/<int:photo_id>/', frontend_views.add_comment, name="add_comment"),
    path('like/<int:photo_id>/', frontend_views.like_photo, name="like_photo"),
    path('save/<int:photo_id>/', frontend_views.save_photo, name="save_photo"),

    # User Profile
    path('profile/', frontend_views.profile, name="profile"),
    path('profile/edit/', frontend_views.edit_profile, name="edit_profile"),
    path('profile/change-password/', frontend_views.change_password, name="change_password"),

    # Recommendations
    path('recommendations/', frontend_views.recommendations, name="recommendations"),

    # Auth (Login / Logout)
    path('login/', frontend_views.login_view, name="login"),
    path('logout/', frontend_views.logout_view, name="logout"),
    path('register/', frontend_views.register, name="register"), 

     # Photo Detail View 
   path('photo/<int:photo_id>/', frontend_views.photo_detail, name='photo_detail'),
]
