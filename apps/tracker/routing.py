from django.urls import re_path
from .consumers import *

websocket_urlpatterns = [
     re_path(r'ws/bugtracker/(?P<project_id>\w+)/$', BugTrackerConsumer.as_asgi()),
]
