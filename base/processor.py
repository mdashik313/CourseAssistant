from base.models import Unread_Counts
from chat.views import get_unread_messages_count


def notifications(request):
    user = request.user

    if not user.is_authenticated:
        return {}

    notifications_count = 0
    if not Unread_Counts.objects.filter(user=user).exists():
        Unread_Counts.objects.create(user=user)

    notifications_count = Unread_Counts.objects.filter(user=user)[0].notification
    return {
        'notifications_count': notifications_count,
        'unread_messages_count': get_unread_messages_count(user),
    }
