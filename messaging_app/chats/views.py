#!/usr/bin/env python3
from django.shortcuts import render # type: ignore
"""Views for chats app."""
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .models import Chat
from .serializers import ChatSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .permissions import IsConversationParticipantAndMethodAllowed

class MessageViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsConversationParticipantAndMethodAllowed]

    def handle_no_permission(self):
        return Response({'detail': 'You are not allowed to access this message.'}, status=status.HTTP_403_FORBIDDEN)

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related("participants", "messages")
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']

     def get_queryset(self):
        return Conversation.objects.filter(users=self.request.user)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
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
    queryset = Message.objects.all().select_related("conversation", "sender")
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsOwnerOrReadOnly]
    search_fields = ['sender__username', 'conversation__conversation_id', 'message_body']

    def get_queryset(self):
        # Filters messages by parent chat ID and current user
        return Message.objects.filter(
            chat_id=self.kwargs['chat_pk'],
            conversation__users=self.request.user
        )



