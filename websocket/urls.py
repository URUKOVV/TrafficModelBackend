from django.urls import path
from .consumers import TrafficModelConsumer

ws_urlpatterns = [
    path('ws/traffic-model/', TrafficModelConsumer.as_asgi())
]
