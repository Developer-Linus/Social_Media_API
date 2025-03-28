from django.urls import path
from .views import CreateNotificationView, ListNotificationsView, MarkNotificationAsRead


urlpatterns = [
    path('notifications/', ListNotificationsView.as_view(),name='notifications'),
    path('notificaitons/post/', CreateNotificationView.as_view(),name='notification'),
    path('notifications/<int:pk>/mark-as-read/', MarkNotificationAsRead.as_view(), name='mark_as_read'),
]