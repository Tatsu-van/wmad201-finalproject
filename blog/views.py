from django.shortcuts import get_object_or_404, redirect, render

from django.db.models import Count, Q, query
from django.http import Http404
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import generic

from django.urls import reverse_lazy

from .forms import PostCreateForm

from blog.models import ContentImage, Post, Category, Tag

# Create your views here.

def home(request):
    return render(request, 'blog/home.html')


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.is_public and not self.request.user.is_authenticated:
            raise Http404
        return obj

class PostUpdateView(generic.UpdateView):
    template_name = 'blog/post_update.html'
    model = Post
    form_class = PostCreateForm
    
    def get_success_url(self):
        return reverse_lazy('blog:home', kwargs={'pk': self.object.pk})


class PostDeleteView(generic.DeleteView):
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy('blog:home')


class IndexView(ListView):
    model = Post
    template_name = 'blog/home.html'
    paginate_by = 5


class CategoryListView(ListView):
    queryset = Category.objects.annotate(
        num_posts=Count('post', filter=Q(post__is_public=True)))


class TagListView(ListView):
    queryset = Tag.objects.annotate(num_posts=Count(
        'post', filter=Q(post__is_public=True)))


class CategoryPostView(ListView):
    model = Post
    template_name = 'blog/category_post.html'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(Category, slug=category_slug)
        qs = super().get_queryset().filter(category=self.category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagPostView(ListView):
    model = Post
    template_name = 'blog/tag_post.html'

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        qs = super().get_queryset().filter(tags=self.tag)
        return qs

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['tag'] = self.tag
      return context

class PostCreateView(generic.CreateView):
    model = Post 
    form_class = PostCreateForm 
    content_image = ContentImage
    success_url = reverse_lazy('blog:home') 

class SerachPostView(ListView):
    model = Post
    template_name = 'blog/search_post.html'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        lookups = (
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query)
        )

        if query is not None:
            qs = super().get_queryset().filter(lookups).distinct()
            return qs

        qs = super().get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context