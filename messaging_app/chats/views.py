#!/usr/bin/env python3
from django.shortcuts import render # type: ignore
"""Views for chats app."""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating conversations.
    """
    queryset = Conversation.objects.all().prefetch_related("participants", "messages")
    serializer_class = ConversationSerializer

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """
        Custom endpoint to send a message to this conversation.
        """
        conversation = self.get_object()
        data = request.data.copy()
        data['conversation'] = str(conversation.conversation_id)
        data['sender'] = request.user.pk if request.user.is_authenticated else None
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save(conversation=conversation, sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating messages.
    """
    queryset = Message.objects.all().select_related("conversation", "sender")
    serializer_class = MessageSerializer

