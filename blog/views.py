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
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy('blog:home')


class PostDeleteView(generic.DeleteView):
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy('blog:home')


class IndexView(ListView):
    model = Post
    template_name = 'blog/home.html'


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
    template_name = 'blog/tag_post.hrml'

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        qs = super().get_queryset().filter(tag=self.tag)
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

# def PostCreateView(request):
#     if request.method == 'POST':
#         form = PostCreateForm(request.POST)

#         if form.is_valid():
#             post = Post()

#             post.tags = request.POST['tags']
#             post.title = request.POST['title']
#             post.image = request.FILES['image']
#             post.content = request.POST['content']
#             post.description = request.POST['description']
#             post.published_at = timezone.now()
#             post.is_public = request.POST['is_published']
#             category_obj = Category.objects.get(name=post.category)
#             post.category_obj = category_obj
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostCreateForm()

#     return render(request, 'blog/post_form.html', {'form': form})