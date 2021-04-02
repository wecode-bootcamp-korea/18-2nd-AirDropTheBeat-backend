from django.http                  import JsonResponse
from django.views                 import View
from django.db.models.aggregates  import Avg
from django.db.models.query_utils import Q

from room.models import Room

class RoomListView(View):
    #@status_decorator
    def get(self, request):
        city_id     = request.GET.get('city_id', None)
        district_id = request.GET.get('district_id', None)
        start_date  = request.GET.get('start_date', None) 
        end_date    = request.GET.get('end_date', None) 
        guest       = request.GET.get('guest', None) 

        page        = int(request.GET.get('page', 1))
        item        = 20
        offset      = (page-1) * item
        limit       = offset + item

        #user_id = request.user_id
        user_id   = 1
        rooms     = Room.objects.filter(Q(city_id=city_id)|Q(district_id=district_id)|Q(maximum_people=guest))
        room_list = [{
                "room_id"           : room.id,
                "titile"            : room.title,
                "type_id"           : room.type_id,
                "type_name"         : room.type.name,
                "city_name"         : room.city.name,
                "district_name"     : room.district.name,
                "price"             : room.price,
                "discount_rate"     : room.discount_rate,
                "latitude"          : room.latitude,
                "longitude"         : room.longitude,
                "room_info"         : [room.maximum_people, room.bedroom, room.bed, room.bathroom],
                "room_conveniences" : [convenience.name for convenience in room.room_conveniences.all()],
                "avg_review"        : review_average(room),
                "count_review"      : room.reviews.count(),
                "wish"              : True,
                "images"            : [images.image_url for images in room.image_set.all()], 
            } for room in rooms[offset:limit]]
        return JsonResponse({'room_list':room_list}, status=200)

def review_average(room):
    if room.review_set.exists():
        sum_rating = room.review_set.aggregate(cleanliness=Avg('cleanliness'))['cleanliness'] +\
                    room.review_set.aggregate(accuracy=Avg('accuracy'))['accuracy'] +\
                    room.review_set.aggregate(communication=Avg('communication'))['communication'] +\
                    room.review_set.aggregate(location=Avg('location'))['location'] +\
                    room.review_set.aggregate(checkin=Avg('checkin'))['checkin'] +\
                    room.review_set.aggregate(satisfaction=Avg('satisfaction'))['satisfaction']
        rating     = round(sum_rating/6,2)
        return rating
    else:
        return 0