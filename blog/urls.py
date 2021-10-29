from django.urls import path

from blog.views import IndexView, PostDetailView, CategoryListView, TagListView, CategoryPostView, TagPostView, PostCreateView,PostUpdateView, PostDeleteView, home

app_name = 'blog'
urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    # path('home', IndexView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post_update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('post_delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('category/<str:category_slug>/',
         CategoryPostView.as_view(), name='category_post'),
    path('tag/<str:tag_slug>/', TagPostView.as_view(), name='tag_post'),
    path('post_create', PostCreateView.as_view(), name='post_create'),
]