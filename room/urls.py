
from django.urls import path

from room.views import RoomListView

urlpatterns = [
    path('', RoomListView.as_view())
]
