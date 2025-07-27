# chats/middleware.py
from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        path = request.path
        time = datetime.now()

        with open("requests.log", "a") as f:
            f.write(f"{time} - User: {user} - Path: {path}\n")

        return self.get_response(request)
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now()
        current_hour = now.hour

        # Only allow access between 18 (6PM) and 21 (9PM)
        if not (18 <= current_hour < 21):
            return HttpResponseForbidden("Access to chat is restricted at this time.")

        return self.get_response(request)