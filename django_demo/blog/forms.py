
from django import forms
from .models import Comment

#
from .models import Post

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'video']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')

        if not content and not image and not video:
            raise forms.ValidationError("Please provide either content, image, or video.")
        elif content and (image and video):
            raise forms.ValidationError("Please provide either content or image or video, not both.")
        elif image and video:
            raise forms.ValidationError("Please provide either image or video, not both.")

        return cleaned_data



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
