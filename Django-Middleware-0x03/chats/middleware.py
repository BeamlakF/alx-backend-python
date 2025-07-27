# chats/middleware.py
from datetime import datetime
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from datetime import datetime, timedelta
from collections import defaultdict

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



class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_log = defaultdict(list)
        self.offensive_words = ['badword', 'uglyword']  # Extend as needed

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/api/'):
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Clean up old timestamps
            self.ip_message_log[ip] = [
                timestamp for timestamp in self.ip_message_log[ip]
                if now - timestamp < timedelta(minutes=1)
            ]

            # Rate limiting
            if len(self.ip_message_log[ip]) >= 5:
                return JsonResponse(
                    {"error": "Rate limit exceeded. Max 5 messages per minute."},
                    status=429
                )

            # Offensive word check
            if request.content_type == 'application/json':
                try:
                    import json
                    body = json.loads(request.body)
                    message = body.get('message', '')
                    if any(word in message.lower() for word in self.offensive_words):
                        return JsonResponse(
                            {"error": "Offensive language detected. Message blocked."},
                            status=403
                        )
                except Exception:
                    pass  # If parsing fails, ignore silently

            # Add this message timestamp
            self.ip_message_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check for restricted paths (e.g., /api/admin-actions/)
        if request.path.startswith('/api/admin-actions/'):
            user = request.user
            if not user.is_authenticated or not hasattr(user, 'role'):
                return HttpResponseForbidden("No role assigned or user not authenticated.")

            if user.role not in ['admin', 'moderator']:
                return HttpResponseForbidden("Insufficient role permissions.")

        return self.get_response(request)
