from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from pictale_app.models import DailyPhoto, Comment, Like, SavedPhoto, User, PhotoRecommendation
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django import forms


# ----------------------------
# Home Page
# ----------------------------
def home(request):
    # Get photos ordered by latest featured
    daily_photo = DailyPhoto.objects.order_by('-date_featured').first()
    return render(request, "pictale_app/home.html", {"daily_photo": daily_photo})


# ----------------------------
# Like a Photo
# ----------------------------
@login_required
def like_photo(request, photo_id):
    photo = get_object_or_404(DailyPhoto, id=photo_id)
    like, created = Like.objects.get_or_create(user=request.user, post=photo)
    # If already liked, ignore (no duplicates because of unique_together)
    return redirect("home")

# ----------------------------
# Add Comment
# ----------------------------
@login_required
def add_comment(request, photo_id):
    if request.method == "POST":
        photo = get_object_or_404(DailyPhoto, id=photo_id)
        comment_text = request.POST.get("comment_text")
        if comment_text:
            Comment.objects.create(user=request.user, post=photo, comment_text=comment_text, created_at=timezone.now())
    return redirect("home")

# ----------------------------
# Save a Photo
# ----------------------------
@login_required
def save_photo(request, photo_id):
    photo = get_object_or_404(DailyPhoto, id=photo_id)

    # Check if already saved
    if SavedPhoto.objects.filter(user=request.user, post=photo).exists():
        messages.info(request, "📌 You’ve already saved this photo.")
    else:
        SavedPhoto.objects.create(user=request.user, post=photo)
        messages.success(request, "💾 Photo saved successfully!")

    return redirect("home")


# ----------------------------
# Profile Page
# ----------------------------
@login_required
def profile(request):
    saved_photos = SavedPhoto.objects.filter(user=request.user).select_related("post")
    return render(request, "pictale_app/profile.html", {
        "user": request.user,
        "saved_photos": saved_photos
    })


# ----------------------------
# Edit Profile
# ----------------------------
@login_required
def edit_profile(request):
    if request.method == "POST":
        request.user.username = request.POST.get("username", request.user.username)
        request.user.email = request.POST.get("email", request.user.email)
        request.user.bio = request.POST.get("bio", request.user.bio)
        
        if "profile_picture" in request.FILES:
            request.user.profile_picture = request.FILES["profile_picture"]

        request.user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("profile")

    return render(request, "pictale_app/edit_profile.html", {"user": request.user})


# ----------------------------
# Change Password
# ----------------------------
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # keep session alive
            messages.success(request, "Password changed successfully!")
            return redirect("profile")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "pictale_app/change_password.html", {"form": form})


# ----------------------------
# Photo Recommendations
# ----------------------------
@login_required
def recommendations(request):
    if request.method == "POST":
        title = request.POST.get("title")
        story = request.POST.get("story")
        image_file = request.FILES.get("image_file")

        PhotoRecommendation.objects.create(
            user=request.user,
            title=title,
            story=story,
            image_file=image_file
        )
        messages.success(request, "Recommendation submitted for review!")
        return redirect("recommendations")

    recs = PhotoRecommendation.objects.filter(user=request.user)
    return render(request, "pictale_app/recommendations.html", {"recommendations": recs})


# ----------------------------
# Login / Logout / Register
# ----------------------------
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()
    return render(request, "pictale_app/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "pictale_app/register.html", {"form": form})

# ----------------------------
# Display a single photo
# ----------------------------
def photo_detail(request, photo_id):
    photo = get_object_or_404(DailyPhoto, id=photo_id)
    return render(request, 'pictale_app/photo_detail.html', {'photo': photo})




