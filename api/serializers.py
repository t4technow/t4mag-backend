from rest_framework import serializers
from blog.models import Category, Post, Tag
from users.models import User
from analytics.models import PostVisit, Visitor

class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'profile_pic')

class UserSerializer(serializers.ModelSerializer):
  following_authors = UserFollowingSerializer(many=True)
  class Meta:
    model = User
    fields = ('username', 'email', 'first_name', 'last_name', 'is_superuser', 'is_author', 'bio', 'profile_pic', 'following_authors')

class UserSerializerUtil(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'profile_pic')

class CategorySerializerUtil(serializers.ModelSerializer):
  
  class Meta:
    model = Category
    fields = ('title', 'slug')

class PostSerializerUtil(serializers.ModelSerializer):
  category = CategorySerializerUtil(many=False)
  author = UserSerializerUtil(read_only=True)

  class Meta:
    model = Post
    fields = ('id', 'title', 'slug', 'excerpt', 'author', 'category', 'created_at', 'thumbnail_sm_url', 'thumbnail_url', 'views')
    

class CategorySerializer(serializers.ModelSerializer):
  post_count = serializers.SerializerMethodField()
  
  def get_post_count(self, obj):
    return obj.post_category.filter(status='published').count()
  class Meta:
    model = Category
    fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_posts(self, category):
        posts = category.post_category.filter(status='published')
        return PostSerializerUtil(posts, many=True).data
      
class CategoryLatestPostSerializer(serializers.ModelSerializer):
  latest_post = serializers.SerializerMethodField()

  class Meta:
    model = Category
    fields = '__all__'

  def get_latest_post(self, obj):
    post = obj.post_category.filter(status='published').order_by('-created_at').first()
    if post:
        return PostSerializerUtil(post, many=False).data
    return None

class TagSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Tag
    fields = '__all__'

class TagDetailSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = '__all__'

    def get_posts(self, tag):
        posts = tag.post_tags.filter(status='published')
        return PostSerializerUtil(posts, many=True).data


class PostSerializer(serializers.ModelSerializer):
  author = UserSerializer(read_only=True)
  category = CategorySerializer(many=False)

  class Meta:
    model = Post
    fields = ('id', 'title', 'slug', 'excerpt', 'author', 'category', 'created_at', 'thumbnail_sm_url', 'thumbnail_url', 'views')
    
class AllPostSerializer(serializers.ModelSerializer):
  author = serializers.ReadOnlyField(source="author.username")
  category = CategorySerializer(many=False)

  class Meta:
    model = Post
    fields = ('id', 'title', 'slug', 'excerpt', 'author', 'category', 'created_at', 'thumbnail_sm_url', 'thumbnail_url', 'views', 'status')

class PostDetailSerializer(serializers.ModelSerializer):
  author = UserSerializer()
  category = CategorySerializer(many = False)
  tags = TagSerializer(many=True) 

  previous_post = serializers.SerializerMethodField()
  next_post = serializers.SerializerMethodField()

  class Meta:
    model = Post
    fields = ('id', 'title', 'slug', 'featured_image_url', 'thumbnail_sm_url', 'thumbnail_url', 'body', 'excerpt', 'author', 'category', 'tags', 'created_at', 'status', 'content_type', 'views', 'previous_post', 'next_post')

  def get_previous_post(self, obj):
    previous_post = Post.postobjects.filter(status='published', created_at__lt=obj.created_at).order_by('-created_at').first()
    return PostSerializer(previous_post).data if previous_post else None

  def get_next_post(self, obj):
    next_post = Post.postobjects.filter(status='published', created_at__gt=obj.created_at).order_by('created_at').first()
    return PostSerializer(next_post).data if next_post else None

class PostVisitSerializer(serializers.ModelSerializer):
  post = serializers.ReadOnlyField(source="post.title")
  total_views = serializers.SerializerMethodField()
  
  class Meta:
    model = PostVisit
    fields = '__all__'
  
  def get_total_views(self, obj):
    return obj.post.views
  

class VisitorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Visitor
    fields = '__all__'