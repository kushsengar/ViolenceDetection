import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LivePredictionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("live_predictions", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("live_predictions", self.channel_name)

    async def send_prediction(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"prediction": message}))
