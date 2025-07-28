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

def message_thread_view(request, message_id):
    # Fetch the root message with sender and receiver info
    root_message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver').prefetch_related('replies'),
        pk=message_id
    )

    # Recursive function to build the thread
    def build_thread(message):
        replies = message.replies.all().select_related('sender', 'receiver').prefetch_related('replies')
        return {
            'message': message,
            'replies': [build_thread(reply) for reply in replies]
        }

    thread = build_thread(root_message)
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
