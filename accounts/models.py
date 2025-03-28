from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _ # Used for translation based on user's language

class CustomUserManager(BaseUserManager):
    'Custom user model where email will be used for authentication'
    def create_user(self,username, email, password=None, **extra_fields):
        if not email:
            return ValueError(_('The email must be set.'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        # Create a superuser with given email and password
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            return ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            return ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
        
class CustomUser(AbstractUser):
    username= models.CharField(max_length=255, default='user', null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    profile_picture=models.ImageField(upload_to='profile/', null=True, blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='followed_by', blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='following_users', blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    address = models.TextField(null=True)
    phone_number = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return f'Profile for {self.user.email}'