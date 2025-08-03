from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_project(project_id, content,type,action):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'project_{project_id}',
        {
            'type': type,
            'content': content,
            'action':action
        }
    )



def notify_users(user_id, content):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {
            "type": "new_comment",
            "content": content,
        }
    )