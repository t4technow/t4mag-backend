from .models import Post

class PostViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # check if the current request is for a post detail page
        if request.path.startswith('/api/posts/') and request.path.split('/')[-2] !='posts' and request.method == 'GET':
            # get the post ID from the URL
            post_slug = request.path.split('/')[-2]
            # check if the user has already viewed this post in this session
            if 'viewed_posts' not in request.session:
                request.session['viewed_posts'] = set()
            if post_slug not in request.session['viewed_posts']:
                # increment the view count for the post
                post = Post.objects.get(slug=post_slug)
                post.views += 1
                post.save()
                # mark the post as viewed in this session
                request.session['viewed_posts'].add(post_slug)

        response = self.get_response(request)

        return response