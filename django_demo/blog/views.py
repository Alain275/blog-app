from django.forms.models import BaseModelForm
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from .models import Post, Comment
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.views.generic import (
ListView,
DetailView,
CreateView,
UpdateView,
DeleteView,
)



from .forms import CommentForm,BlogPostForm






# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'home.html', context)
from django.contrib.auth.decorators import login_required

# @login_required
# def LikeView(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     if request.user.is_authenticated:
#         post.likes.add(request.user)
#     return HttpResponseRedirect(reverse('blog-home'))

# def UnlikeView(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
    
#     if request.user in post.likes.all():
#             # User has already liked the post, remove the like
#             post.likes.remove(request.user)
#     return HttpResponseRedirect(reverse('blog-home'))


@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user

    if user in post.likes.all():
        # User has already liked the post, so unlike it
        post.likes.remove(user)
    else:
        # User hasn't liked the post, so like it
        post.likes.add(user)

    # Redirect back to the post or another appropriate page
    return HttpResponseRedirect(reverse('blog-home'))




class PostListView(ListView):
    model = Post
    template_name='home.html' #<model>_<viewtype>.html
    context_object_name='posts'
    print(model)
    

    ordering = ['-date_posted']
    paginate_by = 4

class UserPostListView(ListView):
    model = Post
    template_name='post_list.html' #<model>_<viewtype>.html
    context_object_name='posts'
    paginate_by = 5

    def get_queryset(self):
        user= get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted') 

def PostDetailView(request, pk):
    context = {}
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post=post)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()

    context['comments'] = comments
    context['new_comment'] = new_comment
    context['comment_form'] = comment_form
    context['post'] = post

    return render(request, 'post_detail.html', context)
    

def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('blog-home')  # Redirect to your blog post list view
    else:
        form = BlogPostForm()

    return render(request, 'post_form.html', {'form': form})
   
    
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content','image','video']
    template_name='post_form.html' #<model>_<viewtype>.html   

    def form_valid(self,form):
        form.instance.author= self.request.user
        return super().form_valid(form) 
    
    def test_func(self):
        post= self.get_object()
        if self.request.user == post.author:
          return True
        return False   
    
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post  
    template_name='post_comfirm_delete.html' #<model>_<viewtype>.html   
    success_url='/'
    def test_func(self):
        post= self.get_object()
        if self.request.user == post.author:
          return True
        return False    
    
    
def about(request):
    return render(request, 'about.html', {'title': 'About'})

def password_reset_confirm(request):
    return render(request, 'password_reset_confirm.html')




