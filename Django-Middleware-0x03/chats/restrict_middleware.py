from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        # Restrict access outside 6PM (18:00) to 9PM (21:00)
        if not (now >= now.replace(hour=18, minute=0, second=0, microsecond=0) and now <= now.replace(hour=21, minute=0, second=0, microsecond=0)):
            return HttpResponseForbidden('Access to chat is restricted outside 6PM to 9PM.')
        return self.get_response(request)
