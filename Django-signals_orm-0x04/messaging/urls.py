from django.urls import path
from .views import delete_user
from .views import get_thread

urlpatterns = [
    path('delete_user/', delete_user, name='delete_user'),
    path('thread/<int:message_id>/', get_thread, name='get_thread'),
]
