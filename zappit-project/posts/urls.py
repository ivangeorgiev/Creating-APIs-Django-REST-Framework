from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
  path('posts/', views.PostList.as_view(), name='posts-list'),
  path('posts/<int:pk>/', views.PostRetrieveUpdateDestroy.as_view(), name='posts-update'),
  path('posts/<int:post_id>/vote/', views.PostVoteCreate.as_view(), name='post-vote'),
]
