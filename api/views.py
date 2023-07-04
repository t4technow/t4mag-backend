from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.middleware.csrf import get_token

from django.db.models import Max
  
from blog.models import Post, Category
from users.models import User
from analytics.models import PostVisit, Visitor

from .serializers import *

class CsrfTokenView(APIView):
    def get(self, request):
        csrf_token = get_token(request)
        return Response({'csrfToken': csrf_token})

class PostList(generics.ListAPIView):
  queryset = Post.postobjects.all()
  serializer_class = PostSerializer
  
class PopularPosts(generics.ListAPIView):
  queryset = Post.postobjects.all().order_by('-views')
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
  queryset = Post.postobjects.all().order_by('-created_at')
  serializer_class = PostSerializer
  
class CategoryList(generics.ListAPIView):
  queryset = Category.objects.all()
  lookup_field = 'slug'
  serializer_class = CategorySerializer
  
class CategoryDetails(generics.RetrieveUpdateAPIView):
  queryset = Category.objects.all()
  lookup_field = 'slug'
  serializer_class = CategoryDetailSerializer
  
class CategoryLatestPost(generics.ListAPIView):
  queryset = Category.objects.all()
  lookup_field = 'slug'
  serializer_class = CategoryLatestPostSerializer

  def get_queryset(self):
    queryset = super().get_queryset()
    queryset = queryset.annotate(latest_post=Max('post_category__created_at'))
    return queryset.order_by('-latest_post')
  
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
  
  
from django.http import JsonResponse
from urllib.parse import urljoin

def upload_image(request):
    if request.method == 'POST':
        image_urls = []
        for file in request.FILES.getlist('file'):
            # Process each file and save it to your desired location
            # Generate the image URL based on the image name or any relevant logic
            image_name = file.name  # Assuming the image name is the same as the uploaded file name
            base_url = 'http://127.0.0.1:5555/media/post/blob/'  # Base URL for your images
            image_url = urljoin(base_url, image_name)
            image_urls.append(image_url)
        return JsonResponse({'imageUrls': image_urls})
    return JsonResponse({'error': 'Invalid request'})