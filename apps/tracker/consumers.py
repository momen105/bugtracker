import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BugTrackerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get project_id from URL route parameters
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.room_group_name = f'project_{self.project_id}'
        self.user = self.scope['user']

        # User-specific group name for private notifications
        self.user_group_name = f"user_{self.user.id}"

        # Join project group for bug updates and comments
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # Join user group for personal notifications
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave project group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        # Leave user group
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        # Handle typing indicator event
        if data.get("type") == "typing":
            # Broadcast typing to project group excluding sender
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_indicator',
                    'user': data['user'],
                    'sender_channel': self.channel_name,
                }
            )

       
    # Handler for project-wide bug updates (create/update)
    async def bug(self, event):
        content = event.get("content")
        action = event.get("action")

        await self.send(text_data=json.dumps({
            "type": "bug",
            "action": action,
            "content": content,
        }))

    # Handler for new comment event
    async def new_comment(self, event):
        await self.send(text_data=json.dumps({
            'type': 'comment',
            'comment': event,
        }))

    # Handler for typing indicator event
    async def typing_indicator(self, event):
        # Avoid sending typing notification back to sender
        if event['sender_channel'] != self.channel_name:
            await self.send(text_data=json.dumps({
                'type': 'typing',
                'user': event['user'],
            }))
