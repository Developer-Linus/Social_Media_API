from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from.models import Notification
from.serializers import NotificationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

# Create a notification view
class CreateNotificationView(APIView):
    def post(self, request, *args, **kwargs):
        # Get the data from the request
        data = request.data
        
        # Create a new notification
        Notification.objects.create(
            recipient= generics.get_object_or_404(User, pk=data['recipient_id']),
            actor = generics.get_object_or_404(User, pk=data['actor_id']),
            verb = data['verb'],
            target_content_type_id = data['target_content_type_id'],
            target_object_id = data['target_object_id']
        )
        
        # Return a success response
        return Response({'message': 'Notification created successfully.'}, status=status.HTTP_201_CREATED)

# Fetching notifications view
class ListNotificationsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        queryset = Notification.objects.filter(self.request.user)
        return queryset
# View for marking Notification as read
class MarkNotificationAsRead(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        # Get the notification id
        pk = kwargs['notification_id']
        # Get the notification object
        notification = generics.get_object_or_404(Notification, pk=pk)
        # check if the notification belongs to the request user
        if notification.recipient!= request.user:
            return Response({'message': 'You do not have permission to mark this notification as read'}, status=status.HTTP_403_FORBIDDEN)
        # Check if the notification is already read
        if notification.read:
            return Response({'message': 'You have already read this notification'}, status=status.HTTP_200_OK)
        notification.read = True
        notification.save()
        return Response({'message': 'Notification marked as read'}, status=status.HTTP_200_OK)



