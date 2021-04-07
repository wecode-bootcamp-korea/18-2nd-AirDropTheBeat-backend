from datetime import datetime

from django.views                 import View
from django.http                  import JsonResponse
from django.db.models             import Avg
from django.db.models.query_utils import Q

from room.models import Room, District, Image, RoomConvenience, RoomRule, Review
from user.models import User, Host
from book.models import Book, BookStatus

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


class RoomListView(View):
    def get(self, request):
        try:
            city_id      = request.GET.get('city_id', None)
            district     = request.GET.get('district', None)
            str_checkin  = request.GET.get('checkin', None) 
            str_checkout = request.GET.get('checkout', None)
            checkin      = datetime.strptime(str_checkin, "%Y-%m-%d")
            checkout     = datetime.strptime(str_checkout, "%Y-%m-%d")
            adults       = request.GET.get('adults', 0)
            child        = request.GET.get('child', 0)
            baby         = request.GET.get('baby', 0)
            guest        = int(adults) + int(child) + int(baby)

            exist_district = District.objects.filter(name=district).exists()
            if not exist_district:
                return JsonResponse({'message': 'DISTRICT_DOES_NOT_EXIST'}, status=400)
           
            page   = int(request.GET.get('page', 1))
            item   = 20
            offset = (page-1) * item
            limit  = offset + item
            
            district       = District.objects.get(name=district)
            BOOKED         = BookStatus.objects.get(name="예약완료")
            booked_room_id = [booked.room.id for booked in Book.objects.filter(
                                                                            (Q(start_date__gte = checkin) & Q(start_date__lt = checkout))|
                                                                            (Q(end_date__gt    = checkin) & Q(end_date__lte  = checkout)),
                                                                            book_status = BOOKED
                                                                            ).select_related('room')]
            
            rooms = Room.objects.filter(city_id             = city_id, 
                                        district            = district, 
                                        maximum_people__gte = guest).exclude(id__in = booked_room_id).select_related('type','city','district').prefetch_related('room_conveniences','image_set')

            room_list = [{
                     "room_id"           : room.id,
                     "title"             : room.title,
                     "type_id"           : room.type_id,
                     "type_name"         : room.type.name,
                     "city_name"         : room.city.name,
                     "district_name"     : room.district.name,
                     "price"             : room.price,
                     "discount_rate"     : room.discount_rate,
                     "latitude"          : float(room.latitude),
                     "longitude"         : float(room.longitude),
                     "room_info"         : "최대인원 {0}명•침실{1}개•침대 {2}개•욕실 {3}개".format(room.maximum_people, room.bedroom, room.bed, room.bathroom),
                     "room_conveniences" : [convenience.name+" " for convenience in room.room_conveniences.all()],
                     "avg_review"        : review_average(room),
                     "count_review"      : room.reviews.count(),
                     "images"            : [images.image_url for images in room.image_set.all()], 
                 } for room in rooms[offset:limit]]

            return JsonResponse({'room_list':room_list}, status=200)
        
        except TypeError:
            return JsonResponse({'message': 'TYPE_ERROR'}, status=400)


def review_average(room):
    if room.review_set.exists():
        room.select_related('review_set')
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
