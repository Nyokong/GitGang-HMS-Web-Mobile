import json
from channels.generic.websocket import WebsocketConsumer
from .models import FeedbackMessage

class FeedbackConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'message': 'Hello, WebSocket!'
        }))

    def disconnect(self, close_code):
        pass

    def message(self, text_data):
        # we get the text json data here
        text_data_json = json.loads(text_data)

        # so we get the message and save it to the feedback model
        message = FeedbackMessage(message=text_data_json['message'])
        print("websocket msg: ",message)

        # trigger the save method
        message.save()

        self.send(text_data=json.dumps({
            'message': f"Saved: {text_data_json['message']}"
        }))

    # async def chat_message(self, event):
    #     message = event['message']
    #     await self.send(text_data=json.dumps({
    #         'message': message
    #     }))
