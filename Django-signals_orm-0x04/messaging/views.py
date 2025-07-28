from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db import transaction

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        with transaction.atomic():
            user.delete()
        return redirect('logout')  # Redirect to logout or homepage after deletion
    return HttpResponse("Send a POST request to delete your account.")
