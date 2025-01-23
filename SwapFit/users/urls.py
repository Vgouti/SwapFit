from django.urls import path
from .views import register, like_post,add_comment,login_view,logout_view,explore, unfollow_user,follow_user,foryou,profile,edit_profile,search_users,view_profile,admin_dashboard,admin_transactions,admin_profiles,admin_posts,delete_post

urlpatterns = [
    path('register/', register, name='register'),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('explore/', explore, name='explore'),
    path('foryoupage/', foryou, name='foryoupage'),
    path('profile/',profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('search/', search_users, name='search_users'),
    path('profile/<str:username>/',view_profile, name='view_profile'),
    path('profile/<str:username>/follow/', follow_user, name='follow_user'),
    path('profile/<str:username>/unfollow/', unfollow_user, name='unfollow_user'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('comment/<int:post_id>/',add_comment, name='add_comment'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin_posts/', admin_posts, name='admin_posts'),
    path('admin_posts/delete/<int:post_id>/', delete_post, name='delete_post'),
    path('admin_profiles/', admin_profiles, name='admin_profiles'),
    path('admin_transactions/', admin_transactions, name='admin_transactions'),
]
