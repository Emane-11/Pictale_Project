from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from pictale_app.models import DailyPhoto, Comment, Like, SavedPhoto
from django.contrib import messages
from django.utils import timezone

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

