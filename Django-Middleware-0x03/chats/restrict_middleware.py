from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Example: Block access between 12 AM (0) and 6 AM (5)
        if 0 <= current_hour < 6:
            return HttpResponseForbidden("Access is restricted between 12 AM and 6 AM.")
        return self.get_response(request)
