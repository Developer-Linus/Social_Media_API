from rest_framework import serializers
from .models import Post, Comment, Like
from accounts.serializers import CustomUserSerializer

# Post serializer
class PostSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at']
    def validate(self, data):
        title = data.get('title')
        content = data.get('content')
        if title is None or len(title)<=8:
            raise serializers.ValidationError('Post title must be more than 8 characters.')
        if content is None or len(content) <= 10:
            raise serializers.ValidationError('Post content must be more than 10 characters.')
        return data

# Comment serializer
class CommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content']
    
    def validate(self, data):
        content = data.get('content')
        if content is None or content<=5:
            raise serializers.ValidationError('Comment must be at least 5 characters long')
        return data
    
# Like serializer
class LikeSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']

    