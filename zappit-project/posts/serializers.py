from rest_framework import serializers
from .models import (
  Post,
  Vote,
)

class PostSerializer(serializers.ModelSerializer):
  poster = serializers.ReadOnlyField(source='poster.username')
  poster_id = serializers.ReadOnlyField(source='poster.id')
  num_votes = serializers.SerializerMethodField()

  class Meta:
    model = Post
    fields = ('post_id', 'title', 'url', 'poster', 'poster_id', 'created_at', 'num_votes')

  def get_num_votes(self, post):
    return post.votes.all().count()
    return Vote.objects.filter(post=post).count()


class VoteSerializer(serializers.ModelSerializer):
  # voter = serializers.ReadOnlyField(source='voter.username')
  # voter_id = serializers.ReadOnlyField(source='voter.id')
  class Meta:
    model = Vote
    fields = ('post_id', )
