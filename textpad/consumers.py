# consumers.py
import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("A client is trying to connect...")
        self.accept()
        print(f"Client connected: {self.channel_name}")

    def disconnect(self, close_code):
        print(f"Client disconnected: {self.channel_name}")

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')

        # Echo the message back to the client
        self.send(text_data=json.dumps({
            'message': message
        }))
