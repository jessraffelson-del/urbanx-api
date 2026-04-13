import json
from channels.generic.websocket import AsyncWebsocketConsumer


class CityEventConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'city_events'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'city_event',
                'message': data
            }
        )

    async def city_event(self, event):
        await self.send(text_data=json.dumps(event['message']))