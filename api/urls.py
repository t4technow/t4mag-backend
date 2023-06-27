from django.urls import path
from .views import *

urlpatterns = [
  path('', AllPosts.as_view(), name='all_posts'),
  path('posts/', PostList.as_view(), name='post_list'),
  path('posts/create/', PostCreate.as_view(), name='post_create'),
  path('posts/recent/', RecentPosts.as_view(), name='recent_posts'),
  path('posts/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
  path('categories/', CategoryList.as_view(), name='categories_list'),
  path('users/', UsersList.as_view(), name="users_list"),
  path('authors/', AuthorList.as_view(), name="authors_list"),
  path('analytics/', Analytics.as_view(), name='analytics'),
  path('analytics/visitors', Visitors.as_view(), name='visitors_analytics'),
  
]