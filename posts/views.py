from django.shortcuts import render
from django.views import View
from .models import Post

# Create your views here.
class PostListView(View):
    def get(self, request, *args, **kwargs): # will run whenevr the user tries to ciew this page
        posts = Post.objects.all().order_by('-created_on') # displays posts from the most recent to the last (newest to oldest)

        context = {
            'post_list' : posts,
        }
        
        return render(request, 'social/post_list.html', context)
