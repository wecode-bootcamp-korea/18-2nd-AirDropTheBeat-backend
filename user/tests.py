import json, bcrypt

from mock import patch, MagicMock

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
    
    
class SignInTest(TestCase):
    def setUp(self):
        hashed_password = bcrypt.hashpw("123456789".encode('utf-8'), bcrypt.gensalt())
        db_password     = hashed_password.decode('utf-8')

        User.objects.create(first_name    = "sehyeong",
                            last_name     = "kim",
                            date_of_birth = "19961210",
                            email         = "sshkim96@gmail.com",
                            password      = db_password,
                            phone_number  = "01099264524",
                            )

    def tearDown(self):
        User.objects.all().delete()

    def test_signin_user_success(self): 
        data = {
                "email":"sshkim96@gmail.com",
                "password":"123456789"
                }

        response = client.post('/user/signin', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_signin_user_does_not_exist(self):
        data = {
                "email":"wecode@gmail.com",
                "password":"1234567"
                }

        response = client.post('/user/signin', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_signin_key_error(self):
        data = {
                "email":"sshkim96@gmail.com"
                }

        response = client.post('/user/signin', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_signin_jsondecode_error(self):
        data = {}

        response = client.post('/user/signin', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)


class KakaoSignInTest(TestCase):
    def setUp(self):
        User.objects.create(
                            first_name = "세형",
                            last_name  = "김",
                            email      = "sshkim96@gmail.com",
                            password   = "1234567"
                            )

        User.objects.create(
                            email    = "tkddus614@naver.com",
                            kakao_id = 3784375
                            )

    def tearDown(self):
        User.objects.all().delete()

    @patch('user.views.requests')
    def test_kakao_signin_create_user_success(self, mocked_request):

        class MockedResponse:
            def json(self):
                return {
                        "id": 547834,
                        "kakao_account": {
                            "email": "haha@gmail.com"
                            }
                        }

        mocked_request.get = MagicMock(return_value = MockedResponse())
        headers  = {'HTTP_Authorization': 'fake_token'}
        response = client.get('/user/signin-kakao', content_type='application/json', **headers)

        self.assertEqual(response.status_code, 200)

    @patch('user.views.requests')
    def test_kakao_signin_get_user_success(self, mocked_request):

        class MockedResponse:
            def json(self):
                return {
                        "id": 3784375,
                        "kakao_account": {
                            "email": "tkddus614@naver.com"
                            }
                        }
        mocked_request.get = MagicMock(return_value = MockedResponse())
        headers  = {'HTTP_Authorization': 'fake_token'}
        response = client.get('/user/signin-kakao', content_type='application/json', **headers)

        self.assertEqual(response.status_code, 200)

    @patch('user.views.requests')
    def test_kakao_signin_email_already_exists(self, mocked_request):

        class MockedResponse:
            def json(self):
                return {
                        "id":3423423,
                        "kakao_account": {
                            "email": "sshkim96@gmail.com"
                            }
                        }

        mocked_request.get = MagicMock(return_value = MockedResponse())
        headers  = {'HTTP_Authorization': 'fake_token'}
        response = client.get('/user/signin-kakao', content_type='application/json', **headers)
        
        message = response.json()['message']
        self.assertEqual(message, 'USER_EMAIL_ALREADY_EXISTS')

    @patch('user.views.requests')
    def test_kakao_signin_invalid_kakao_token(self, mocked_request):

        class MockedResponse:
            def json(self):
                return {
                        "code": -401
                        }

        mocked_request.get = MagicMock(return_value=MockedResponse())
        headers  = {'HTTP_Authorization': 'fake_token'}
        response = client.get('/user/signin-kakao', content_type='application/json', **headers)

        message = response.json()['message']
        self.assertEqual(message, 'INVALID_TOKEN')

    @patch('user.views.requests')
    def test_kakao_sign_in_key_error(self, mocked_request):
        
        class MockedResponse:
            def json(self):
                return {
                        }

        mocked_request.get = MagicMock(return_value=MockedResponse())
        headers  = {'HTTP_Authorization': 'fake_token'}
        response = client.get('/user/signin-kakao', content_type='application/json', **headers)

        message = response.json()['message']
        self.assertEqual(message, 'KEYERROR')

    @patch('user.views.requests')
    def test_token_does_not_exist(self, mocked_request):
        
        class MockedResponse:
            def json(self):
                return {
                        "id": 123
                        }

        mocked_request.get = MagicMock(return_value=MockedResponse())
        response = client.get('/user/signin-kakao', content_type='application/json')
        
        message = response.json()['message']
        self.assertEqual(message, 'TOKEN_DOES_NOT_EXIST')
