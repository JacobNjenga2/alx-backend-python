import logging
from datetime import datetime
import time
from django.http import HttpResponseForbidden
from collections import defaultdict, deque

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('request_logger')

        handler = logging.FileHandler('requests.log')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)

        if not self.logger.hasHandlers():
            self.logger.addHandler(handler)

        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_log = defaultdict(deque)  # {ip: deque([timestamp,...])}
        self.limit = 5
        self.window = 60  # seconds

    def __call__(self, request):
        # Only count POST requests to chat endpoints
        if request.method == 'POST' and request.path.startswith('/chat'):
            ip = self.get_client_ip(request)
            now = time.time()
            log = self.ip_message_log[ip]
            # Remove timestamps older than window
            while log and now - log[0] > self.window:
                log.popleft()
            if len(log) >= self.limit:
                return HttpResponseForbidden('Message limit exceeded. Try again later.')
            log.append(now)
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

