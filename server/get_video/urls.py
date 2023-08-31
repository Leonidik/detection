# get_video/urls.py

from django.urls import path, include
from .views import select_video, index, livefe

urlpatterns = [
    path('', select_video, name='select_video'),    
    path('index/', index,  name='index'),
    path('livefe/<path:path_to_video>', livefe, name="live_camera"),
    
]

