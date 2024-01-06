from django.urls import path
from . import views
from .views import( 
PostListView,
PostDetailView,

PostUpdateView,
PostDeleteView,
UserPostListView,

create_blog_post,
like_post

 

)


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView, name='post-detail'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', create_blog_post, name='blog_post_list'),
    path('about/', views.about, name='blog-about'),
    path ('post/like/<int:post_id>',like_post, name='like_post'),
    # path('post/unlike/<int:post_id>/', UnlikeView, name='unlike_post'),
    
    
   
   
]
