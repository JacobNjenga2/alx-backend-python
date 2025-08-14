#!/usr/bin/env python3
"""Views for chats app."""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os
from datetime import datetime
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Chat, Conversation, Message
from .serializers import ChatSerializer, ConversationSerializer, MessageSerializer
from .permissions import (
    IsOwnerOrReadOnly,
    IsConversationParticipantAndMethodAllowed
)
from .auth import get_authenticated_user
from .filters import MessageFilter
from .pagination import MessagePagination
from .models import Message
from .serializers import MessageSerializer
import django_filters.rest_framework



class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related("participants",
     "messages")
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']


    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        user = get_authenticated_user(request)
        data = request.data.copy()
        data['conversation'] = str(conversation.conversation_id)
        data['sender'] = user.pk

        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save(conversation=conversation, sender=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().select_related("conversation", "sender")
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = MessagePagination
    filterset_class = MessageFilter
    permission_classes = [IsAuthenticated, IsConversationParticipantAndMethodAllowed]
    search_fields = ['sender__username', 'conversation__conversation_id', 'message_body']

    def get_queryset(self):
        return Message.objects.filter(
            chat_id=self.kwargs['chat_pk'],
            conversation__users=self.request.user
        )

    def handle_no_permission(self):
        return Response(
            {'detail': 'You are not allowed to access this message.'},
            status=status.HTTP_403_FORBIDDEN
        )


@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """
    Health check endpoint for Kubernetes liveness and readiness probes
    """
    try:
        # Basic health indicators
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": os.environ.get("APP_VERSION", "unknown"),
            "debug": os.environ.get("DEBUG", "False"),
            "database": "connected",  # You can add actual DB check here
            "checks": {
                "database": True,
                "application": True,
                "environment": True
            }
        }
        
        # Return 200 OK for healthy status
        return JsonResponse(health_status, status=200)
        
    except Exception as e:
        # Return 500 for unhealthy status
        error_status = {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "checks": {
                "database": False,
                "application": False,
                "environment": False
            }
        }
        return JsonResponse(error_status, status=500)



