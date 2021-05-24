import json
import time

import redis
from time import sleep
from django.conf import settings

from channels.generic.websocket import WebsocketConsumer


class TrafficModelConsumer(WebsocketConsumer):
    alive = False

    def connect(self):
        self.alive = True
        self.accept()
        redis_instance = redis.StrictRedis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, password=settings.REDIS_PASSWORD
        )
        while self.alive:
            time_start = time.perf_counter_ns()
            redis_data = redis_instance.get('cars')
            self.send(redis_data.decode('utf-8'))
            sleep_time = 0.167 - time.perf_counter_ns() - time_start * 1e-9
            if sleep_time > 0.0:
                sleep(sleep_time)

    def close(self, code=None):
        self.alive = False
        return super().close(code=code)

    def disconnect(self, code):
        self.alive = False
        return super().disconnect(code)
