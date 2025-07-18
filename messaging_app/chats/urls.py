from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ChatViewSet, MessageViewSet


# Primary router for top-level chats
router = DefaultRouter()
router.register(r'chats', ChatViewSet, basename='chat')

# Nested router for messages under chats
nested_router = NestedDefaultRouter(router, r'chats', lookup='chat')
nested_router.register(r'messages', MessageViewSet, basename='chat-messages')

urlpatterns = [
    path('', include(router.urls)),
]


