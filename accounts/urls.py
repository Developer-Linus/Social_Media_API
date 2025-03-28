from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/<int:pk>', views.TokenView.as_view(), name='token'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='view_profile'),
    path('follow/<int:user_id>', views.FollowView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', views.UnfollowView.as_view(), name='unfollow'),
]