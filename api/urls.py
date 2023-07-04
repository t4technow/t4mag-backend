from django.urls import path
from .views import *

urlpatterns = [
  path('', AllPosts.as_view(), name='all_posts'),
  path('posts/', PostList.as_view(), name='post_list'),
  path('posts/create/', PostCreate.as_view(), name='post_create'),
  path('posts/recent/', RecentPosts.as_view(), name='recent_posts'),
  path('posts/popular/', PopularPosts.as_view(), name='popular_posts'),
  path('posts/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
  path('categories/', CategoryList.as_view(), name='categories_list'),
  path('categories/<slug:slug>/', CategoryDetails.as_view(), name='single_category'),
  path('categories/posts/latest/', CategoryLatestPost.as_view(), name='category_latest_post'),
  path('tags/', TagList.as_view(), name='tags_list'),
  path('tags/<slug:slug>/', TagDetails.as_view(), name='single_tag'),
  path('users/', UsersList.as_view(), name="users_list"),
  path('authors/', AuthorList.as_view(), name="authors_list"),
  path('analytics/', Analytics.as_view(), name='analytics'),
  path('analytics/visitors/', Visitors.as_view(), name='visitors_analytics'),
  
  path('upload-image/', upload_image, name='upload_image'),
  path('get-csrf-token/', CsrfTokenView.as_view(), name='get_token'),
  
]