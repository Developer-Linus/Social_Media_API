from rest_framework import viewsets, permissions, pagination, filters, status, generics
from .models import Post, Comment, Like
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# Custom pagination class 
class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10 # Number of objects to display per page
    page_size_query_param = 'page_size' # Parameter to specifiy page size in query
    max_page_size = 100 # Maximum page size

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['title']
    
    def get_permissions(self):
        if self.action in ['update', 'partial-update', 'destroy', 'create']:
            permission_classes = [permissions.IsAuthenticated]
        else: 
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
    # perform-create method is used to customize instance creation
    # Here, we have used to define author as the request.user
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_permissions(self):
        if self.action in ['update', 'partial-update', 'destroy', 'create']:
            permission_classes = [permissions.IsAuthenticated]
        else: 
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

class FeedAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        current_user = request.user
        following_users = current_user.following.all()
        
        # Get the posts from the users the current follower is following
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        # serialize the posts
        serializer = PostSerializer(posts, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
# Like View
class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    # Handle POST request to /like/ endpoint
    def post(self, request, *args, **kwargs):
        # Get the post id from the request
        pk = kwargs['pk']
        # Get the post object from the database
        post = generics.get_object_or_404(Post, pk=pk)
        # Get the user  making the request
        user = request.user
        # Retrieve a like if exists or create a new one
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({'error' : 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new notification object
        notification = Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='liked',
            target=post
        )
        # Return a success message
        Response({'message': 'Post liked successfully.'}, status=status.HTTP_201_CREATED)

# Unlike view
class UnlikeView(APIView):
    # Allow only authenticated users to unlike
    permission_classes = [permissions.IsAuthenticated]
    
    # Handle the delete request to the /unlike/{post_id}/ endpoint
    def delete(self, request, *args, **kwargs):
        # Get the post id from the URL parameter
        pk = kwargs['pk']
         # Get the post object from the database
        post = generics.get_object_or_404(Post, pk=pk)
        # Get the user making the request
        user = request.user
         # Get the like object from the database
        try:
            like = Like.objects.get(user=user, post=user)
        except Like.DoesNotExist:
            return Response({'error': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)
        
        like.delete()
        
        # Delete the notification object
        try:
            notification = Notification.objects.get(recipient=post.author, actor=user, verb='liked', target=post)
            notification.delete()
        except Notification.DoesNotExist:
            pass
        return Response({'message':'Post unliked successfully.'}, status=status.HTTP_200_OK)
        
    
        
        
        
    
    