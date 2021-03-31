import json, bcrypt, re, requests
from django.db.models.query_utils import Q

from django.views import View
from django.http  import JsonResponse
from json.decoder import JSONDecodeError

from user.models import User
from my_settings import REGEX_NAME, REGEX_DATE_OF_BIRTH, REGEX_EMAIL, REGEX_PASSWORD, REGEX_PHONE_NUMBER

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            first_name    = data['first_name']
            last_name     = data['last_name']
            date_of_birth = data['date_of_birth']
            email         = data['email']
            password      = data['password']
            phone_number  = data.get('phone_number', None)

            if not re.match(REGEX_NAME,first_name) or not re.match(REGEX_NAME,last_name):
                return JsonResponse({"message":"INVALID NAME CHARACTER"}, status = 400)
            if not re.match(REGEX_DATE_OF_BIRTH,date_of_birth):
                return JsonResponse({'message':'DATE_OF_BITRH VALIDATION ERROR'}, status=400)
            if not re.match(REGEX_EMAIL,email):
                return JsonResponse({'message':'EMAIL VALIDATION ERROR'}, status=400)
            if not re.match(REGEX_PASSWORD,password):
                return JsonResponse({'message':'PASSWORD VALIDATION ERROR'}, status=400)
            if phone_number and not re.match(REGEX_PHONE_NUMBER,phone_number):
                return JsonResponse({'message':'PHONE NUMBER VALIDATION ERROR'}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message':'EMAIL ALREADY EXISTS'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode()

            User.objects.create(
                first_name    = first_name,
                last_name     = last_name,
                date_of_birth = date_of_birth,
                email         = email,
                password      = hashed_password,
                phone_number  = phone_number
            )   
            return JsonResponse({'message':'SUCCESS'}, status = 201)
        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message':'JSON DECODE ERROR'}, status=400)