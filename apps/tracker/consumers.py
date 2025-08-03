import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BugTrackerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.room_group_name = f'project_{self.project_id}'

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Optionally handle typing indicator
        if data.get("type") == "typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_indicator',
                    'user': data['user']
                }
            )

    async def bug_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'bug_update',
            'message': event['message']
        }))

    async def new_comment(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_comment',
            'comment': event['comment']
        }))

    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user': event['user']
        }))
