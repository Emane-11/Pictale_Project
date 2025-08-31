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
def home(request, photo_id=None):
    # Get all photos, ordered by latest featured
    all_photos = DailyPhoto.objects.order_by('-date_featured')
    
    if not all_photos:
        # If there are no photos at all, render the page with no photo
        return render(request, "pictale_app/home.html", {"daily_photo": None})

    # Find the current photo
    if photo_id:
        daily_photo = get_object_or_404(DailyPhoto, id=photo_id)
    else:
        # Default to the most recent photo
        daily_photo = all_photos.first()

    # Get a list of all photo IDs in the sorted order
    all_photo_ids = list(all_photos.values_list('id', flat=True))
    
    # Find the index of the current photo
    try:
        current_index = all_photo_ids.index(daily_photo.id)
    except ValueError:
        # This case should not happen if the photo is found, but as a safeguard
        current_index = 0

    # Determine previous and next photo IDs
    previous_photo_id = None
    if current_index < len(all_photo_ids) - 1:
        previous_photo_id = all_photo_ids[current_index + 1]

    next_photo_id = None
    if current_index > 0:
        next_photo_id = all_photo_ids[current_index - 1]
    
    context = {
        "daily_photo": daily_photo,
        "previous_photo_id": previous_photo_id,
        "next_photo_id": next_photo_id,
    }
    
    return render(request, "pictale_app/home.html", context)


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
        comment_text = request.POST.get('comment_text')
        if comment_text:
            Comment.objects.create(post=photo, user=request.user, comment_text=comment_text)
    return redirect("home")

# ----------------------------
# Save a Photo
# ----------------------------
@login_required
def save_photo(request, photo_id):
    photo = get_object_or_404(DailyPhoto, id=photo_id)
    saved_photo, created = SavedPhoto.objects.get_or_create(user=request.user, post=photo)
    if created:
        messages.success(request, f"'{photo.title}' has been saved to your profile.")
    else:
        messages.info(request, f"'{photo.title}' is already saved.")
    return redirect("home")
    
# ----------------------------
# User Profile
# ----------------------------
@login_required
def profile(request):
    saved_photos = SavedPhoto.objects.filter(user=request.user)
    return render(request, "pictale_app/profile.html", {"saved_photos": saved_photos})

@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = forms.UserChangeForm(request.POST, instance=request.user)
        request.user.bio = request.POST.get('bio')
        if 'profile_picture' in request.FILES:
            request.user.profile_picture = request.FILES['profile_picture']
        request.user.save()
        messages.success(request, "Your profile has been updated.")
        return redirect('profile')
    
    return render(request, 'pictale_app/edit_profile.html', {})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'pictale_app/change_password.html', {'form': form})
    
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
    return render(request, "pictale_app/photo_detail.html", {"photo": photo})




