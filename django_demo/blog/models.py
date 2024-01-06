from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User
from django.urls import reverse

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.post.id)])

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default =timezone.now ) 
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,related_name='blog_posts')
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    video = models.FileField(upload_to='blog_videos', null=True, blank=True)
    
    
    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])

    def total_likes(self):
        return self.likes.count()


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})



