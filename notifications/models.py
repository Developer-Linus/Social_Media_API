from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()

class Notification(models.Model):
    # user to receive the notification
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_received')
    # user who performed an action to trigger notification
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_acted')
    # The action that triggered notification
    verb = models.CharField(max_length=255)
    # The object that the notification is about
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')
    read = models.BooleanField(default=False)
    # The date and time the notification was created
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} {self.verb} {self.target}'
