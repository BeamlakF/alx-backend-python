from django.shortcuts import render

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Message
from django.shortcuts import get_object_or_404

@login_required
@require_POST
def delete_user(request):
    user = request.user
    user.delete()
    return JsonResponse({'message': 'User and related data deleted successfully.'})

def get_thread(request, message_id):
    root = get_object_or_404(Message, id=message_id)

    def get_replies(message):
        replies = message.replies.all().order_by('created_at')
        return [
            {
                'id': reply.id,
                'content': reply.content,
                'sender': reply.sender.username,
                'created_at': reply.created_at,
                'replies': get_replies(reply)
            }
            for reply in replies
        ]

    thread = {
        'id': root.id,
        'content': root.content,
        'sender': root.sender.username,
        'created_at': root.created_at,
        'replies': get_replies(root)
    }

    return JsonResponse(thread, safe=False)

def get_threaded_messages(request):
    messages = Message.objects.filter(receiver=request.user)\
        .select_related('sender', 'receiver', 'parent_message')\
        .prefetch_related('replies')
    
    return render(request, 'messages/threaded.html', {'messages': messages})
