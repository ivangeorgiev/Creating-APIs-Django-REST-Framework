from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
  post_id = models.BigAutoField(primary_key=True)
  title = models.CharField(max_length=100)
  url = models.URLField()
  poster = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ('-created_at',)

class Vote(models.Model):
  vote_id = models.BigAutoField(primary_key=True)
  voter = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes')
  voted_at = models.DateTimeField(auto_now_add=True)
