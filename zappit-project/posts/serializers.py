from rest_framework import serializers
from .models import (
  Post,
  Vote,
)

class PostSerializer(serializers.ModelSerializer):
  poster = serializers.ReadOnlyField(source='poster.username')
  poster_id = serializers.ReadOnlyField(source='poster.id')
  class Meta:
    model = Post
    fields = ('post_id', 'title', 'url', 'poster', 'poster_id', 'created_at')

class VoteSerializer(serializers.ModelSerializer):
  # voter = serializers.ReadOnlyField(source='voter.username')
  # voter_id = serializers.ReadOnlyField(source='voter.id')
  class Meta:
    model = Vote
    fields = ('post_id', )
