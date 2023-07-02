from rest_framework import generics
from blog.models import Post, Category
from users.models import User
from analytics.models import PostVisit, Visitor
from .serializers import *

class PostList(generics.ListAPIView):
  queryset = Post.postobjects.all()
  serializer_class = PostSerializer
  
class AllPosts(generics.ListAPIView):
  queryset = Post.objects.all()
  serializer_class = AllPostSerializer

class PostDetail(generics.RetrieveUpdateAPIView):
  queryset = Post.postobjects.all()
  lookup_field = 'slug'
  serializer_class = PostDetailSerializer

class PostCreate(generics.CreateAPIView):
  queryset = Post.objects.all()
  serializer_class = PostDetailSerializer
  
class RecentPosts(generics.ListAPIView):
  queryset = Post.postobjects.all().order_by('created_at')
  serializer_class = PostSerializer
  
class CategoryList(generics.ListAPIView):
  queryset = Category.objects.all()
  lookup_field = 'slug'
  serializer_class = CategorySerializer
  
class CategoryDetails(generics.RetrieveUpdateAPIView):
  queryset = Category.objects.all()
  lookup_field = 'slug'
  serializer_class = CategoryDetailSerializer
  
class TagList(generics.ListAPIView):
  queryset = Tag.objects.all()
  lookup_field = 'slug'
  serializer_class = TagSerializer
  
class TagDetails(generics.RetrieveUpdateAPIView):
  queryset = Tag.objects.all()
  lookup_field = 'slug'
  serializer_class = TagDetailSerializer
  
class UsersList(generics.ListAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  
class AuthorList(generics.ListAPIView):
  queryset = User.authors.all()
  serializer_class = UserSerializer
  
class Analytics(generics.ListAPIView):
  queryset = PostVisit.objects.all()
  serializer_class = PostVisitSerializer
  
class Visitors(generics.ListAPIView):
  queryset = Visitor.objects.all()
  serializer_class = VisitorSerializer