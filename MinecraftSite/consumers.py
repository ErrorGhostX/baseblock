import json
from channels.generic.websocket import AsyncWebsocketConsumer
from minecraft.models import Event

class ParticipantConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.event_id = self.scope['url_route']['kwargs']['event_id']
        self.room_group_name = f'event_{self.event_id}'

        # Присоединяемся к группе событий
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Отключаемся от группы событий
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Получаем сообщение из WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        participant_data = data['participant']

        # Отправляем данные в группу
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'participant_message',
                'participant': participant_data
            }
        )

    # Получаем сообщение от группы
    async def participant_message(self, event):
        participant = event['participant']

        # Отправляем данные в WebSocket
        await self.send(text_data=json.dumps({
            'participant': participant
        }))
