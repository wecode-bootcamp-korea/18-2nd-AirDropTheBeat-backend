from django.urls import path, include

urlpatterns = [
    path('room', include('room.urls')),
    path('user', include('user.urls'))
]
