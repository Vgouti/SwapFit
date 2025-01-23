from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Like, Comment, Follower
from django.contrib.auth.models import User

# Create Post View
@login_required
def create_post(request):
    if request.method == "POST":
        image = request.FILES.get('image')
        caption = request.POST.get('caption')
        if image and caption:
            Post.objects.create(user=request.user, image=image, caption=caption)
            messages.success(request, "Post created successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please provide both an image and a caption.")
    return render(request, 'createpost.html')
 