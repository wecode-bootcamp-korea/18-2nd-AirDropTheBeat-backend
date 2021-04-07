from datetime import datetime

from django.test import TestCase,Client

from user.models import User, Host
from room.models import Room, Type, CheckinType, City, District, AddressLine, Review
from book.models import Book, BookStatus

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



class RoomListViewTest(TestCase):
    def setUp(self):
        city         = City.objects.create(id=1,name="서울시")
        district     = District.objects.create(id=1,city=city, name="강남구")
        address_line = AddressLine.objects.create(id=1,city=city,district=district, name="역삼동")
        checkin      = CheckinType.objects.create(id=1,name="셀프체크인", description="셀프체크인으로 편하게 이용하세요.")
        type         = Type.objects.create(id=1,name="집 전체", description="집 전체를 제공합니다.")
        type2        = Type.objects.create(id=2,name="개인실", description="개인실을 제공합니다.")
        type3        = Type.objects.create(id=3,name="호텔 객실", description="호텔 객실을 제공합니다.")
        user         = User.objects.create(id=1,first_name="sehyeong")
        host         = Host.objects.create(id=1,user=user,residence="서울시 강남구", language="한국어, 영어", available_hour="12:00~18:00")
        book_status  = BookStatus.objects.create(id=1,name="예약완료")

        room1 = Room.objects.create(
                                    id             = 1,
                                    title          = "집1",
                                    type           = type,
                                    host           = host,
                                    checkin        = checkin,
                                    city           = city,
                                    district       = district,
                                    address_line   = address_line,
                                    zip_code       = "1234",
                                    price          = 10000,
                                    discount_rate  = 0,
                                    latitude       = 35.94054,
                                    longitude      = 125.532434,
                                    maximum_people = 2,
                                    checkin_time   = "15:00:00",
                                    checkout_time  = "12:00:00",
                                    bedroom        = 1,
                                    bathroom       = 1,
                                    bed            = 1
                                    )
        room2 = Room.objects.create(
                                    id             = 2,
                                    title          = "집2",
                                    type           = type,
                                    host           = host,
                                    checkin        = checkin,
                                    city           = city,
                                    district       = district,
                                    address_line   = address_line,
                                    zip_code       = "23121",
                                    price          = 91049,
                                    discount_rate  = 0,
                                    latitude       = 35.03453,
                                    longitude      = 125.45523,
                                    maximum_people = 4,
                                    checkin_time   = "15:00:00",
                                    checkout_time  = "12:00:00",
                                    bedroom        = 2,
                                    bathroom       = 1,
                                    bed            = 2
                                    )
        room3 = Room.objects.create(
                                    id             = 3,
                                    title          = "집3",
                                    type           = type,
                                    host           = host,
                                    checkin        = checkin,
                                    city           = city,
                                    district       = district,
                                    address_line   = address_line,
                                    zip_code       = "24443",
                                    price          = 70000,
                                    discount_rate  = 0,
                                    latitude       = 36.42930,
                                    longitude      = 126.53454,
                                    maximum_people = 3,
                                    checkin_time   = "15:00:00",
                                    checkout_time  = "12:00:00",
                                    bedroom        = 1,
                                    bathroom       = 1,
                                    bed            = 1
                                    )
        room4 = Room.objects.create(
                                    id             = 4,
                                    title          = "집4",
                                    type           = type,
                                    host           = host,
                                    checkin        = checkin,
                                    city           = city,
                                    district       = district,
                                    address_line   = address_line,
                                    zip_code       = "42432",
                                    price          = 98000,
                                    discount_rate  = 0,
                                    latitude       = 36.653463,
                                    longitude      = 126.5636,
                                    maximum_people = 2,
                                    checkin_time   = "15:00:00",
                                    checkout_time  = "12:00:00",
                                    bedroom        = 1,
                                    bathroom       = 1,
                                    bed            = 1
                                    )
        
        room5 = Room.objects.create(
                                    id             = 5,
                                    title          = "집5",
                                    type           = type2,
                                    host           = host,
                                    checkin        = checkin,
                                    city           = city,
                                    district       = district,
                                    address_line   = address_line,
                                    zip_code       = "42432",
                                    price          = 53000,
                                    discount_rate  = 0,
                                    latitude       = 36.653463,
                                    longitude      = 126.5636,
                                    maximum_people = 4,
                                    checkin_time   = "15:00:00",
                                    checkout_time  = "12:00:00",
                                    bedroom        = 2,
                                    bathroom       = 1,
                                    bed            = 1
                                    )
        
        room6 = Room.objects.create(
                                    id             = 6,
                                    title          = "집6",
                                    type           = type3,
                                    host           = host,
                                    checkin        = checkin,
                                    city           = city,
                                    district       = district,
                                    address_line   = address_line,
                                    zip_code       = "42432",
                                    price          = 120000,
                                    discount_rate  = 0,
                                    latitude       = 36.653463,
                                    longitude      = 126.5636,
                                    maximum_people = 3,
                                    checkin_time   = "15:00:00",
                                    checkout_time  = "12:00:00",
                                    bedroom        = 2,
                                    bathroom       = 1,
                                    bed            = 1
                                    )


        Book.objects.create(
                            id               = 1,
                            room             = room4,
                            user             = user,
                            book_status      = book_status,
                            number_of_guests = 2,
                            start_date       = datetime(2021,4,18),
                            end_date         = datetime(2021,4,20),
                            serial_number    = "123456"
                            )
        Book.objects.create(
                            id               = 2,
                            room             = room2,
                            user             = user,
                            book_status      = book_status,
                            number_of_guests = 2,
                            start_date       = datetime(2021,4,12),
                            end_date         = datetime(2021,4,16),
                            serial_number    = "45353453"
                            )
        Book.objects.create(
                            id               = 3,
                            room             = room3,
                            user             = user,
                            book_status      = book_status,
                            number_of_guests = 2,
                            start_date       = datetime(2021,4,13),
                            end_date         = datetime(2021,4,15),
                            serial_number    = "524523524"
                            )
        Book.objects.create(
                            id               = 4,
                            room             = room1,
                            user             = user,
                            book_status      = book_status,
                            number_of_guests = 2,
                            start_date       = datetime(2021,4,16),
                            end_date         = datetime(2021,4,18),
                            serial_number    = "5232412"
                            )

    def tearDown(self):
        User.objects.all().delete()
        Host.objects.all().delete()
        City.objects.all().delete()
        District.objects.all().delete()
        AddressLine.objects.all().delete()
        Type.objects.all().delete()
        CheckinType.objects.all().delete()
        Book.objects.all().delete()
        BookStatus.objects.all().delete()


    def test_type_error(self):
        response = client.get('/room/list?city_id=1&district=강남구&adults=2', content_type='application/json')
        self.assertEqual(response.json()['message'], "TYPE_ERROR")

    def test_district_does_not_exist(self):
        response = client.get('/room/list?city_id=1&district=분당구&checkin=2021-04-20&checkout=2021-04-24', content_type='application/json')
        self.assertEqual(response.json()['message'], "DISTRICT_DOES_NOT_EXIST")

    def test_filtering_rooms_success(self):
        response = client.get('/room/list?city_id=1&district=강남구&checkin=2021-04-15&checkout=2021-04-18&adults=2', content_type='application/json')
        self.assertEqual(len(response.json()['room_list']), 4)
        self.assertEqual(response.status_code, 200)

    def test_filtering_rooms_success_with_additional_filter(self):
        response = client.get('/room/list?district=강남구&checkin=2021-04-16&checkout=2021-04-18&typelist=2&typelist=3&min=80000', content_type='application/json')
        self.assertEqual(response.status_code, 200)
