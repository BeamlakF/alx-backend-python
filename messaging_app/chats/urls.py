from django.urls import path, include
from .views import protected_test_view
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, ConversationViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'conversations', ConversationViewSet)

urlpatterns = [
    path('test/', protected_test_view, name='protected-test'),
    path('', include(router.urls)),
]
