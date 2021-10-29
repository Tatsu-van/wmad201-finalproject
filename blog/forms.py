from django import forms
from django.forms import fields
from .models import ContentImage, Post


class PostCreateForm(forms.ModelForm):

    class Meta:
       model = Post
       fields = ('category', 'tags', 'title', 'content','image','is_public')


