from django.views     import View
from django.http      import JsonResponse
from django.db.models import Avg

from room.models import Room, Image, RoomConvenience, RoomRule, Review
from user.models import User, Host

class RoomDetailView(View):
    def get(self, request, room_id):
        checkin_date  = request.GET.get('check_in', None)
        checkout_date = request.GET.get('check_out', None)
        adults        = request.GET.get('adults', 0) 
        child         = request.GET.get('child', 0) 
        baby          = request.GET.get('baby', 0) 

        exist_room = Room.objects.filter(id=room_id).exists()
        if not exist_room:
            return JsonResponse({'message': 'ROOM_DOES_NOT_EXIST'}, status=404)

        room = Room.objects.select_related('city', 'district', 'address_line','type', 'checkin', 'host').prefetch_related('image_set', 'roomconvenience_set', 'roomrule_set').get(id=room_id)

        result = {
                "checkin_date": checkin_date,
                "checkout_date": checkout_date,
                "adult": adults,
                "child": child,
                "baby": baby,
                "number_of_guests": int(adults)+int(child)+int(baby),
                "price": room.price,
                "discount_rate": room.discount_rate,
                "title": room.title,
                "city": room.city.name,
                "district": room.district.name,
                "address_line": room.address_line.name,
                "images_url": [image.image_url for image in room.image_set.all()],
                "type": room.type.name,
                "type_description": room.type.description,
                "maximum_people": room.maximum_people,
                "bedroom": room.bedroom,
                "bathroom": room.bathroom,
                "bed": room.bed,
                "checkin_type": room.checkin.name,
                "checkin_type_description": room.checkin.description,
                "description": room.description,
                "conveniences": [room.convenience.name for room in room.roomconvenience_set.all()],
                "lat": room.latitude,
                "lng": room.longitude,
                "checkin_time": room.checkin_time,
                "checkout_time": room.checkout_time,
                "room_rules": [rule.rule.name for rule in room.roomrule_set.all()],
                "host_id": room.host.id,
                "host_name": room.host.user.first_name,
                "host_image":room.host.user.image_url,
                "host_language": room.host.language,
                "host_available_hour": room.host.available_hour
                }

        return JsonResponse(result, status=200)
        
class ReviewView(View):
    def get(self, request, room_id):
        reviews = Review.objects.filter(room_id=room_id).select_related('user')
        
        if reviews.exists():
            cleanliness   = reviews.aggregate(Avg('cleanliness'))['cleanliness__avg']
            accuracy      = reviews.aggregate(Avg('accuracy'))['accuracy__avg']
            communication = reviews.aggregate(Avg('communication'))['communication__avg']
            location      = reviews.aggregate(Avg('location'))['location__avg']
            checkin       = reviews.aggregate(Avg('checkin'))['checkin__avg']
            satisfaction  = reviews.aggregate(Avg('satisfaction'))['satisfaction__avg']
            total_average = (cleanliness + accuracy + communication + location + checkin + satisfaction)/6
            counts        = reviews.count()

            detail_reviews = [{
                                "id": review.id,
                                "user_id": review.user.id,
                                "user_name": review.user.first_name,
                                "user_image": review.user.image_url if review.user.image_url else [],
                                "created_at": review.created_at,
                                "content": review.content
                                } for review in reviews]

            result = { 
                    "total_average": round(total_average,2),
                    "counts": counts,
                    "cleanliness": round(cleanliness,1),
                    "accuracy": round(accuracy,1),
                    "communication": round(communication,1),
                    "location": round(location,1),
                    "checkin": round(checkin,1),
                    "satisfaction": round(satisfaction,1),
                    "detail_reviews": detail_reviews
                    }
        else:
            result = {}

        return JsonResponse(result, status=200)
