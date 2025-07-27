# chats/middleware.py
from datetime import datetime

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
