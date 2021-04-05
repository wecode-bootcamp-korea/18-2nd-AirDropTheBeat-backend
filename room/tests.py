from django.test import TestCase,Client

from user.models import User, Host
from room.models import Room, Type, CheckinType, City, District, AddressLine, Review

client = Client()
class RoomDetailViewTest(TestCase):
    def setUp(self):
        user = User.objects.create(
                                    first_name = "sehyeong",
                                    last_name  = "kim",
                                    email      = "sshkim96@gmail.com",
                                    password   = "12345678"
                                    )

        room = Room.objects.create(
                                    title          = "서울집",
                                    type           = Type.objects.create(name        = "집전체", 
                                                                         description = "집전체를 사용하게 됩니다."),
                                    host           = Host.objects.create(user           = user,
                                                                         residence      = "서울시 강남구",
                                                                         language       = "한국어, 영어", 
                                                                         available_hour = "12:00~18:00"),
                                    checkin        = CheckinType.objects.create(name        = "셀프 체크인", 
                                                                                description = "셀프 체크인으로 편하게 이용하세요."),
                                    city           = City.objects.create(name="서울시"),
                                    district       = District.objects.create(city = City.objects.create(name = "서울시"),
                                                                             name = "강남구"),
                                    address_line   = AddressLine.objects.create(city     = City.objects.create(name = "서울시"), 
                                                                                district = District.objects.create(city = City.objects.create(name = "서울시"),
                                                                                                                   name = "강남구"), 
                                                                                name     = "역삼동"),
                                    zip_code       = "12346",
                                    description    = "좋은 집",
                                    price          = 140000,
                                    discount_rate  = 0,
                                    latitude       = 37.5047692,
                                    longitude      = 127.0062895,
                                    maximum_people = 2,
                                    checkin_time   = "12:00:00",
                                    checkout_time  = "16:00:00",
                                    bedroom        = 1,
                                    bathroom       = 1,
                                    bed            = 1
                                    )

    def tearDown(self):
        User.objects.all().delete()
        Host.objects.all().delete()
        Room.objects.all().delete()
        City.objects.all().delete()
        Type.objects.all().delete()
        CheckinType.objects.all().delete()
        District.objects.all().delete()
        AddressLine.objects.all().delete()

    def test_get_room_information_success(self):
        response = client.get('/room/2?check_in=2021-04-15&check_out=2021-04-16&adults=1&child=1', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_room_id_does_not_exist(self):
        response = client.get('/room/200', content_type='application/json')
        self.assertEqual(response.status_code, 404)


class ReviewViewTest(TestCase):
    def setUp(self):
        user = User.objects.create(
                                    first_name = "sehyeong",
                                    last_name  = "kim",
                                    email      = "sshkim96@gmail.com",
                                    password   = "12345678"
                                    )

        room = Room.objects.create(
                                    title          = "서울집",
                                    type           = Type.objects.create(name        = "집전체", 
                                                                         description = "집전체를 사용하게 됩니다."),
                                    host           = Host.objects.create(user           = user,
                                                                         residence      = "서울시 강남구",
                                                                         language       = "한국어, 영어", 
                                                                         available_hour = "12:00~18:00"),
                                    checkin        = CheckinType.objects.create(name        = "셀프 체크인", 
                                                                                description = "셀프 체크인으로 편하게 이용하세요."),
                                    city           = City.objects.create(name="서울시"),
                                    district       = District.objects.create(city = City.objects.create(name="서울시"),
                                                                             name = "강남구"),
                                    address_line   = AddressLine.objects.create(city     = City.objects.create(name="서울시"), 
                                                                                district = District.objects.create(city = City.objects.create(name="서울시"),
                                                                                                                   name = "강남구"), 
                                                                                name     = "역삼동"),
                                    zip_code       = "12346",
                                    description    = "좋은 집",
                                    price          = 140000,
                                    discount_rate  = 0,
                                    latitude       = 37.5047692,
                                    longitude      = 127.0062895,
                                    maximum_people = 2,
                                    checkin_time   = "12:00:00",
                                    checkout_time  = "16:00:00",
                                    bedroom        = 1,
                                    bathroom       = 1,
                                    bed            = 1
                                    )
        
        Review.objects.create(
                              user          = User.objects.create(first_name="sehyeong", last_name="kim"),
                              room          = room,
                              content       = "좋아요",
                              cleanliness   = 5,
                              accuracy      = 3,
                              communication = 3,
                              location      = 2,
                              checkin       = 5,
                              satisfaction  = 4
                              )

        Review.objects.create(
                              user          = User.objects.create(first_name="raon", last_name="kim"),
                              room          = room,
                              content       = "강아지가 좋아하는 숙소",
                              cleanliness   = 3,
                              accuracy      = 5,
                              communication = 4,
                              location      = 5,
                              checkin       = 3,
                              satisfaction  = 3
                              )
        
        Review.objects.create(
                              user          = User.objects.create(first_name="code", last_name="we"),
                              room          = room,
                              content       = "위코드",
                              cleanliness   = 4,
                              accuracy      = 2,
                              communication = 5,
                              location      = 5,
                              checkin       = 4,
                              satisfaction  = 3
                              )

    def tearDown(self):
        User.objects.all().delete()
        Host.objects.all().delete()
        Room.objects.all().delete()
        City.objects.all().delete()
        Type.objects.all().delete()
        CheckinType.objects.all().delete()
        District.objects.all().delete()
        AddressLine.objects.all().delete()
        Review.objects.all().delete()

    def test_get_reviews_success(self):
        response = client.get('/room/1/review',content_type='application/json')
        self.assertEqual(response.status_code, 200)

