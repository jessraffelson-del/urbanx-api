from django.urls import re_path
from city import consumers as city_consumers
from marketplace import consumers as marketplace_consumers

websocket_urlpatterns = [
    re_path(r'ws/city/events/$', city_consumers.CityEventConsumer.as_asgi()),
    re_path(r'ws/marketplace/orders/$', marketplace_consumers.OrderConsumer.as_asgi()),
]