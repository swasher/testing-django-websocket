import os
import json
import logging
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

logger = logging.getLogger(__name__)



class LogConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_layer = get_channel_layer()  # Добавляем здесь
        self.LOG_FILE_PATH = os.path.join(settings.BASE_DIR, 'log_file.log')

    async def connect(self):
        await self.channel_layer.group_add('log_updates', self.channel_name)
        await self.accept()
        await self.send_initial_log()  # отправляем стартовый лог после коннекта

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('log_updates', self.channel_name)

    async def send_log_update(self, event):
        log_content = event['content']
        await self.send(text_data=json.dumps({
            'content': log_content,
        }))

    def get_log_file_content(self):
        """Читает содержимое log_file.log."""
        try:
            with open(self.LOG_FILE_PATH, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return ""

    async def send_initial_log(self):
        """Отправляет начальный лог в чаннел."""
        initial_log = self.get_log_file_content()
        log_lines = initial_log.strip().split('\n')
        for line in log_lines:
            await self.channel_layer.send(
                self.channel_name,
                {
                    "type": "send_log_update",
                    "content": line,
                },
            )
