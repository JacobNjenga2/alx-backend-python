from django.contrib.auth.decorators import login_required
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

@login_required
def message_thread_view(request, message_id):
    # Get the root message with all related data
    root_message = Message.objects.filter(pk=message_id)\
        .select_related('sender', 'receiver')\
        .prefetch_related('replies__sender', 'replies__receiver')\
        .first()
    
    if not root_message:
        return HttpResponse("Message not found", status=404)

    # Build the thread structure
    def get_replies(message):
        replies = Message.objects.filter(parent_message=message)\
            .select_related('sender', 'receiver')\
            .prefetch_related('replies')
        
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
