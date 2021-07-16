from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
  path('posts/', views.PostList.as_view(), name='posts-data'),
]
