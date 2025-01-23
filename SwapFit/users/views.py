from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile
from django.contrib import messages
from django.urls import reverse
from wardrobe.models import WardrobeItem
from social.models import Post, Like, Comment, Follower
from transactions.models import Transaction
from random import shuffle
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required

def home(request):
    return render(request, 'home.html')
def foryou(request):
    # Get the logged-in user
    user = request.user

    # Find the users the current user is following
    following_users = Follower.objects.filter(follower=user).values_list('user', flat=True)

    # Get posts from the logged-in user and the users they are following
    posts = Post.objects.filter(user__in=[user.id, *following_users]).order_by('-created_at')

    # Add a flag to indicate if the logged-in user liked each post
    for post in posts:
        post.is_liked_by_user = post.likes.filter(user=user).exists()

    context = {
        'posts': posts,
    }
    return render(request, 'foryoupage.html', context)
def register(request):
    if request.method == 'POST':
        # Fetching form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        bio = request.POST.get('bio')
        location = request.POST.get('location')
        profile_pic = request.FILES.get('profile_pic')

        # Validation
        if not username or not email or not password:
            messages.error(request, "All required fields must be filled.")
            return render(request, 'register.html', {'username': username, 'email': email})

        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'register.html', {'username': username, 'email': email})

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'register.html', {'username': username, 'email': email})

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create user profile
        profile = UserProfile(user=user, gender=gender, bio=bio, location=location, profile_pic=profile_pic)
        profile.save()

        # Automatically log the user in
        login(request, user)
        messages.success(request, "Registration successful!")
        return redirect('foryoupage')  # Replace 'home' with your homepage URL name

    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")

            if user.is_superuser:
                return redirect("admin_dashboard")  # Replace with the URL name for the admin page
            return redirect("foryoupage")  # Replace with your default user page

        messages.error(request, "Invalid username or password.")
        return redirect("login")

    return render(request, "login.html")

@login_required
@staff_member_required
def admin_dashboard(request):
    # Example: Pass data to the template if needed
    users = User.objects.all()
    return render(request, 'admin/admin_dashboard.html', {'users': users})
def is_admin(user):
    return user.is_authenticated and user.is_superuser


@login_required
@user_passes_test(is_admin)
def admin_posts(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'admin/admin_posts.html', context)

@login_required
@user_passes_test(is_admin)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, "The post has been deleted successfully.")
    return redirect('admin_posts')

@login_required
@user_passes_test(is_admin)
def admin_profiles(request):
    # Fetch all users and prefetch their related profiles
    users = User.objects.prefetch_related('profile').all()
    return render(request, 'admin/admin_profiles.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def admin_transactions(request):
    transactions = Transaction.objects.all()
    context = {
        'transactions': transactions,
    }
    return render(request, 'admin/admin_transactions.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")

def explore(request):
    return render(request, 'explore.html')

def profile(request):
    """User Profile Page"""
    user = request.user
    posts = Post.objects.filter(user=user)
    wardrobe_items = WardrobeItem.objects.filter(user=user)
    followers_count = Follower.objects.filter(user=user).count()
    following_count = Follower.objects.filter(follower=user).count()

    context = {
        'user': user,
        'posts': posts,
        'wardrobe_items': wardrobe_items,
        'followers_count': followers_count, 
        'following_count': following_count,
    }
    return render(request, 'profile.html', context)


def edit_profile(request):
    """Edit Profile Page"""
    user = request.user
    profile = user.profile  # Access the related UserProfile instance

    if request.method == 'POST':
        bio = request.POST.get('bio')
        location = request.POST.get('location')
        profile_pic = request.FILES.get('profile_pic')

        # Update profile details
        profile.bio = bio
        profile.location = location
        if profile_pic:
            profile.profile_pic = profile_pic
        profile.save()

        messages.success(request, "Your profile has been updated successfully!")
        return redirect('profile')

    context = {
        'profile': profile,
    }
    return render(request, 'editprofile.html', context)

def search_users(request):
    query = request.GET.get('q')  # Get the search term from the URL
    users = User.objects.filter(username__icontains=query) if query else []
    context = {
        'query': query,
        'users': users,
    }
    return render(request, 'search_results.html', context)
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user)
    
    # Check if the logged-in user is following the profile user
    is_following = False
    if request.user.is_authenticated:
        is_following = Follower.objects.filter(user=user, follower=request.user).exists()
    wardrobe_items = WardrobeItem.objects.filter(user=user)
    context = {
        'profile_user': user,
        'posts': posts,
        'wardrobe_items': wardrobe_items,
        'is_following': is_following,
    }
    return render(request, 'view_profile.html', context)

def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    current_user = request.user

    if target_user == current_user:
        return redirect('view_profile', username=username)

    # Toggle follow/unfollow
    if Follower.objects.filter(user=target_user, follower=current_user).exists():
        # Unfollow
        Follower.objects.filter(user=target_user, follower=current_user).delete()
    else:
        # Follow
        Follower.objects.create(user=target_user, follower=current_user)

    return redirect('view_profile', username=username)

def unfollow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    Follower.objects.filter(follower=request.user, following=target_user).delete()
    return redirect('view_profile', username=username)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
        messages.info(request, "You unliked the post.")
    else:
        messages.success(request, "You liked the post.")
    return redirect('foryoupage')

# Add Comment View
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        text = request.POST.get('text')
        if text:
            Comment.objects.create(user=request.user, post=post, text=text)
            messages.success(request, "Comment added!")
        else:
            messages.error(request, "Comment cannot be empty.")
    return redirect('foryoupage')