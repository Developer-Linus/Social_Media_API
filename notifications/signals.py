from django.db.models.signals import post_save
from django.dispatch import receiver
from.models import Notification
from posts.models import Post
from posts.models import Comment
from posts.models import Like
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=Notification)
def send_notifications(sender, instance, created, **kwargs):
    if created:
        subject = 'New Notification'
        message = f'You have a new notification: {instance.verb}'
        from_email = settings.EMAIL_HOST_USER
        to_email = instance.recipient.email
        send_mail(subject, message, from_email, [to_email])
        print(f'Notification email sent to {instance.recipient.username}')
# Define a signal receiver function that will be triggered when a new post is saved
@receiver(post_save, sender=Post)
def create_post_notification(sender, instance, created, **kwargs):
    """
    This function creates a notification for the post author when a new post is created.
    
    Parameters:
    sender (Post): The model that triggered the signal (Post)
    instance (Post): The instance of the Post model that was saved
    created (bool): A boolean indicating whether the instance was created or updated
    **kwargs: Additional keyword arguments passed to the signal receiver
    """
    # Check if the post was created (not updated)
    if created:
        # Create a new notification for the post author
        Notification.objects.create(
            # Set the recipient of the notification to the post author
            recipient=instance.author,
            # Set the actor of the notification to the post author (since they created the post)
            actor=instance.author,
            # Set the verb of the notification to 'created a new post'
            verb='created a new post',
            # Set the target of the notification to the post instance
            target=instance
        )

# Define a signal receiver function that will be triggered when a new comment is saved
@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """
    This function creates a notification for the post author when a new comment is created.
    
    Parameters:
    sender (Comment): The model that triggered the signal (Comment)
    instance (Comment): The instance of the Comment model that was saved
    created (bool): A boolean indicating whether the instance was created or updated
    **kwargs: Additional keyword arguments passed to the signal receiver
    """
    # Check if the comment was created (not updated)
    if created:
        # Create a new notification for the post author
        Notification.objects.create(
            # Set the recipient of the notification to the post author
            recipient=instance.post.author,
            # Set the actor of the notification to the comment author
            actor=instance.author,
            # Set the verb of the notification to 'commented on your post'
            verb='commented on your post',
            # Set the target of the notification to the comment instance
            target=instance
        )

# Define a signal receiver function that will be triggered when a new like is saved
@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    """
    This function creates a notification for the post author when a new like is created.
    
    Parameters:
    sender (Like): The model that triggered the signal (Like)
    instance (Like): The instance of the Like model that was saved
    created (bool): A boolean indicating whether the instance was created or updated
    **kwargs: Additional keyword arguments passed to the signal receiver
    """
    # Check if the like was created (not updated)
    if created:
        # Create a new notification for the post author
        Notification.objects.create(
            # Set the recipient of the notification to the post author
            recipient=instance.post.author,
            # Set the actor of the notification to the user who liked the post
            actor=instance.user,
            # Set the verb of the notification to 'liked your post'
            verb='liked your post',
            # Set the target of the notification to the like instance
            target=instance
        )