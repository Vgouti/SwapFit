from django.urls import path
from . import views

urlpatterns = [
    path('create-post/', views.create_post, name='create_post'),
    # path('posts/', views.post_list, name='post_list'),
    # path('like/<int:post_id>/', views.like_post, name='like_post'),
    # path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    # path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
]
