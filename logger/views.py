import os
import logging
from django.shortcuts import render
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings

logger = logging.getLogger(__name__)
channel_layer = get_channel_layer()

def index(request):
    return render(request, 'logger/index.html')

def log_view(request):
    return render(request, 'logger/log.html')

def add_name(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            log_message = f"Добавлено имя: {name}"
            logger.info(log_message)
            send_log_to_websocket(log_message)
            return JsonResponse({'status':  'ok'})
    return JsonResponse({'status':  'error'}, status=400)


def send_log_to_websocket(log_message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "log_updates",
        {
            "type": "send_log_update",  # Это имя метода, который будет вызван в LogConsumer
            "content": log_message,
        },
    )

def log(message: str):
    log_message = f"{message}"
    logger.info(log_message)
    send_log_to_websocket(log_message)
