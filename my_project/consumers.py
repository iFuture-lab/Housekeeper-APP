import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
# from login.models import CustomUser

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from login.models import CustomUser
        user_id = self.scope["query_string"].decode("utf-8").split("user_id=")[-1]
        print(user_id)

        try:
            self.user = await database_sync_to_async(CustomUser.objects.get)(id=user_id)
            print(self.user)
            await self.accept()
            self.group_name = f"notifications_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
        except CustomUser.DoesNotExist:
            self.close()
        # self.group_name = f"notifications_{self.scope['user'].id}"

        # await self.channel_layer.group_add(
        #     self.group_name,
        #     self.channel_name
        # )

        # await self.accept()

    async def disconnect(self, close_code):
        # pass
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')

        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def send_notification(self, event):
        notification = event['notification']

        notification['id'] = str(notification['id'])
        if 'users' in notification:
            notification['users'] = [str(uid) for uid in notification['users']]

        await self.send(text_data=json.dumps({
            'notification': notification
        }))