from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db import transaction

User = get_user_model()

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        with transaction.atomic():
            user.delete()
        return redirect('logout')  # Or wherever you want to redirect after deletion
    return HttpResponse("Send a POST request to delete your account.")
