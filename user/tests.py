import json

from django.test import TestCase, Client

from user.models import User

client = Client()
class SignUpTest(TestCase):
    def setUp(self):
        User.objects.create(
            first_name    = 'kookhyun',
            last_name     = 'park',
            date_of_birth = '1990-10-20',
            email         = 'parkgood1020@gmail.com',
            password      = 'parkgood10',
            phone_number  = '010-1234-5678'
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signup_success(self):
        data = {
            "first_name"   :"chan ho",
            "last_name"    :"park",
            "date_of_birth":"1991-03-05",
            "email"        :"park0305@gmail.com",
            "password"     :"parkgood1020"
        }
        response = client.post('/user/signup', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)

    def test_signup_name_valid_error(self):
        data = {
            "first_name"   :"chan ho123",
            "last_name"    :"park",
            "date_of_birth":"1991-03-05",
            "email"        :"park0305@gmail.com",
            "password"     :"parkgood1020"
        }
        response = client.post('/user/signup', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_signup_date_of_birth_valid_error(self):
        data = {
            "first_name"   :"chan ho",
            "last_name"    :"park",
            "date_of_birth":"199103-05",
            "email"        :"park0305@gmail.com",
            "password"     :"parkgood1020"
        }
        response = client.post('/user/signup', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_signup_email_valid_error(self):
        data = {
            "first_name"   :"chan ho",
            "last_name"    :"park",
            "date_of_birth":"1991-03-05",
            "email"        :"park0305gmail.com",
            "password"     :"parkgood1020"
        }
        response = client.post('/user/signup', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_signup_password_valid_error(self):
        data = {
            "first_name"   :"chan ho",
            "last_name"    :"park",
            "date_of_birth":"1991-03-05",
            "email"        :"park0305@gmail.com",
            "password"     :"park"
        }
        response = client.post('/user/signup', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_signup_phone_number_valid_error(self):
        data = {
            "first_name"   :"chan ho",
            "last_name"    :"park",
            "date_of_birth":"1991-03-05",
            "email"        :"park0305@gmail.com",
            "password"     :"parkgood1020",
            "phone_number" :"010-12345678",
        }
        response = client.post('/user/signup', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_signup_email_already_exists_error(self):
        data = {
            "first_name"   :"chan ho",
            "last_name"    :"park",
            "date_of_birth":"1991-03-05",
            "email"        :"parkgood1020@gmail.com",
            "password"     :"parkgood1020",
        }
        response = client.post('/user/signup', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_signup_key_error(self):
        data = {
            "first_name"   :"chan ho",
            "last_name"    :"park",
            "date_of_birth":"1991-03-05",
            "email_address":"park0305@gmail.com",
            "password"     :"parkgood1020"
        }
        response = client.post('/user/signup', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)