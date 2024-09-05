import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import FeedbackMessage

class FeedbackConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'feedback'

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
        # we get the text json data here
        text_data_json = json.loads(text_data)

        # so we get the message and save it to the feedback model
        message = FeedbackMessage(message=text_data_json['message'])
        print("websocket msg: ",message)

        # trigger the save method
        message.save()

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'feedback_message',
                'message': message
            }
        )

    # async def chat_message(self, event):
    #     message = event['message']
    #     await self.send(text_data=json.dumps({
    #         'message': message
    #     }))
