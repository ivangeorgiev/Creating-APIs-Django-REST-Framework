from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Post, Vote
from .serializers import PostSerializer, VoteSerializer

class PostList(generics.ListCreateAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]

  def perform_create(self, serializer):
    serializer.save(poster=self.request.user)

class PostRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]

  def perform_create(self, serializer):
    serializer.save(poster=self.request.user)

  def delete(self, request, *args, **kwargs):
    post = Post.objects.filter(post_id=kwargs['pk'], poster=self.request.user)
    if post.exists():
      return self.destroy(request, *args, **kwargs)
    else:
      raise ValidationError('Post doesn\'t exist or you are not the right person to delete.')


class PostVoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
  serializer_class = VoteSerializer
  permission_classes = [permissions.IsAuthenticated]
  
  def get_queryset(self):
    user = self.request.user
    post = Post.objects.get(post_id=self.kwargs['post_id'])
    return Vote.objects.filter(voter=user, post=post)

  def perform_create(self, serializer):
    if self.get_queryset().exists():
      raise ValidationError('You have already voted for this post.')
    post = Post.objects.get(post_id=self.kwargs['post_id'])
    serializer.save(voter=self.request.user, post=post)

  def delete(self, request, *args, **kwargs):
    if not self.get_queryset().exists():
      raise ValidationError('You haven\'t voted for this post.')
    self.get_queryset().delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

