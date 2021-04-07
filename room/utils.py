from django.db.models import Avg


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
