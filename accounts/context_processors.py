from .models import Message
# create a context processor in order to display the messages number bade.
def load_unread_messages(request):
    unread_messages = Message.objects.all().filter(read=False, reciever_id=request.user.id, sender_id=request.user.id).count()
    return {'unread_messages' : unread_messages}