from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.db import transaction
from .models import Message

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        with transaction.atomic():
            user.delete()
        return redirect('logout')  # Redirect to logout or homepage after deletion
    return HttpResponse("Send a POST request to delete your account.")

@cache_page(60)  # Cache for 60 seconds
@login_required
def message_thread_view(request, message_id):
    # Get the root message with all related data
    root_message = Message.objects.filter(pk=message_id)\
        .select_related('sender', 'receiver')\
        .prefetch_related('replies__sender', 'replies__receiver')\
        .only(
            'id', 
            'content',
            'timestamp',
            'sender__username',
            'receiver__username',
            'edited',
            'edited_at'
        ).first()
    
    if not root_message:
        return HttpResponse("Message not found", status=404)

    # Build the thread structure
    def get_replies(message):
        replies = Message.objects.filter(parent_message=message)\
            .select_related('sender', 'receiver')\
            .prefetch_related('replies')\
            .only(
                'id',
                'content',
                'timestamp',
                'sender__username',
                'receiver__username',
                'edited',
                'edited_at'
            )
        
        return [{
            'message': reply,
            'replies': get_replies(reply)
        } for reply in replies]

    thread = {
        'message': root_message,
        'replies': get_replies(root_message)
    }

    return render(request, 'messaging/thread.html', {'thread': thread})

@login_required
def reply_to_message(request, message_id):
    parent = get_object_or_404(Message, pk=message_id)
    if request.method == "POST":
        content = request.POST.get("content")
        Message.objects.create(
            sender=request.user,
            receiver=parent.receiver,
            content=content,
            parent_message=parent
        )
        return redirect('message_thread_view', message_id=parent.pk)

@login_required
def inbox_view(request):
    # Use the custom UnreadMessagesManager with field optimization
    unread_messages = Message.unread.unread_for_user(request.user)\
        .only(
            'id',
            'content',
            'timestamp',
            'sender__username',
            'read'
        )
    return render(request, 'messaging/inbox.html', {
        'unread_messages': unread_messages
    })
