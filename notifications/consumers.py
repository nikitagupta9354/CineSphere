from channels.generic.websocket import AsyncWebsocketConsumer
import json
import jwt
from django.conf import settings






class MovieNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        token = None
        user_id=None
        for header in self.scope['headers']:
            if header[0] == b'authorization':
                token = header[1].decode('utf-8') 
                break

        if token:
            try:
                decoded_token = jwt.decode(token,settings.SECRET_KEY, algorithms=['HS256'])
                user_id = decoded_token.get('user_id')
            except Exception:
                await self.close()
        else:
            await self.close()
        
        
        await self.accept()
            
        
        self.movie_group_name = 'Movie_notifications'
        await self.channel_layer.group_add(
            self.movie_group_name,
            self.channel_name
            )
            
        self.review_group_name = 'Review_notifications'
        await self.channel_layer.group_add(
            self.review_group_name,
            self.channel_name
            )
            
        self.recommendation_group_name = f'user_{user_id}_recommendation_notifications'
        await self.channel_layer.group_add(
            self.recommendation_group_name,
            self.channel_name
            )
        

    async def disconnect(self, close_code):
        if hasattr(self, 'movie_group_name'):
            await self.channel_layer.group_discard(self.movie_group_name, self.channel_name)
        if hasattr(self, 'review_group_name'):
            await self.channel_layer.group_discard(self.review_group_name, self.channel_name)
        if hasattr(self, 'recommendation_group_name'):
            await self.channel_layer.group_discard(self.recommendation_group_name, self.channel_name)


    # This method will be called when you want to send a notification to all users
    async def send_movie_notification(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'notification':message
        }))

    # This method sends a notification to users who rated a specific movie
    async def send_review_notification(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'notification':message
        }))


    # This method sends a recommendation notification to users who are subscribed
    async def send_recommendation_notification(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'notification':message
        }))
        
