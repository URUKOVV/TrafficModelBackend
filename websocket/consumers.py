import asyncio
import time

import redis
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings


class TrafficModelConsumer(AsyncWebsocketConsumer):
    alive = False
    redis_instance = None
    time_prev = None

    async def connect(self):
        self.alive = True
        await self.accept()
        self.redis_instance = redis.StrictRedis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, password=settings.REDIS_PASSWORD
        )

    async def receive(self, text_data=None, bytes_data=None):
        redis_data = self.redis_instance.get('cars')
        if self.time_prev:
            sleep_time = 0.167 - time.perf_counter_ns() - self.time_prev * 1e-9
            await asyncio.sleep(sleep_time)
        await self.send(redis_data.decode('utf-8'))
        self.time_prev = time.perf_counter_ns()

