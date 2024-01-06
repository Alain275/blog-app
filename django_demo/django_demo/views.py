
from django.shortcuts import render

def blog_post(request):
    # Your existing blog post view logic here
    return render(request, 'blog_post.html')
