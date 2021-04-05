from django.urls import path

from room.views import RoomDetailView, ReviewView 

urlpatterns = [
    path('/<int:room_id>', RoomDetailView.as_view()),
    path('/<int:room_id>/review', ReviewView.as_view()),
]
