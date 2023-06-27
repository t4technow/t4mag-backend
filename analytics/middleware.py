from django.utils.deprecation import MiddlewareMixin
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.conf import settings
from user_agents import parse
from django.urls import resolve

from .models import PostVisit, Visitor
from blog.models import Post


class PostViewMiddleware(MiddlewareMixin):
    def process_request(self, request):
    
        ip_address = request.META.get('REMOTE_ADDR')
        ua_string = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse(ua_string)

        visitor_qs = Visitor.objects.filter(
            browser_family=user_agent.browser.family,
            os_family=user_agent.os.family,
            ip_address=ip_address,
        )
        if not visitor_qs.exists():
            visitor = Visitor.objects.create(
                browser_family=user_agent.browser.family,
                os_family=user_agent.os.family,
                ip_address=ip_address,
            )

        # check if the current request is for a post detail page
        if resolve(request.path_info).url_name == 'post_detail' and request.method == 'GET':
            # get the post ID from the URL
            post_slug = request.path.split('/')[-2]
            
            # check if the user has already viewed this post in this session
            if 'viewed_posts' not in request.session:
                request.session['viewed_posts'] = set()
            if post_slug not in request.session['viewed_posts']:
                # increment the view count for the post
                post_visit = PostVisit.objects.filter(post__slug=post_slug)
                post = Post.objects.get(slug=post_slug)
                post.views += 1
                post.save()
                
                if request.user.is_authenticated:
                    post_visit = post_visit.filter(user=request.user)
                else:
                    post_visit = post_visit.filter(user=None)
                if post_visit.exists():
                    post_visit = post_visit.first()
                    
                    if user_agent.browser.family != post_visit.browser_family or \
                        user_agent.os.family != post_visit.os_family or \
                        ip_address != post_visit.ip_address:
                        # increment the unique view count for the post
                        
                        post_visit.unique_views += 1
                        post_visit.browser_family = user_agent.browser.family
                        post_visit.os_family = user_agent.os.family
                        post_visit.ip_address = ip_address
                        post_visit.last_visit = timezone.now()
                        post_visit.save()
                else:
                    # create a new PostVisit record for this user
                    
                    post_visit = PostVisit.objects.create(
                        post=Post.objects.get(slug=post_slug),
                        user=request.user if request.user.is_authenticated else None,
                        unique_views=1,
                        browser_family=user_agent.browser.family,
                        os_family=user_agent.os.family,
                        ip_address=ip_address,
                        last_visit=timezone.now()
                    )
                
                # mark the post as viewed in this session
                viewed_posts = set(request.session['viewed_posts'])
                viewed_posts.add(post_slug)
                request.session['viewed_posts'] = list(viewed_posts)
        
        return None
    
    def process_response(self, request, response):
        # convert set to list before serializing to JSON
        if 'viewed_posts' in request.session:
            request.session['viewed_posts'] = list(request.session['viewed_posts'])
        
        return response

