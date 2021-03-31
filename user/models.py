from django.db import models

class User(models.Model):
    first_name    = models.CharField(max_length=30, null=True)
    last_name     = models.CharField(max_length=20, null=True)
    date_of_birth = models.CharField(max_length=45, null=True)
    email         = models.EmailField(max_length=100, null=True, unique=True)
    password      = models.CharField(max_length=300, null=True)
    phone_number  = models.CharField(max_length=20, null=True)
    image_url     = models.URLField(max_length=3000, null=True)
    kakao_id      = models.BigIntegerField(null=True, unique=True)

    class Meta:
        db_table = "users"

class Host(models.Model):
    user           = models.ForeignKey('User', on_delete=models.CASCADE)
    residence      = models.CharField(max_length=45)
    language       = models.CharField(max_length=45)
    available_hour = models.EmailField(max_length=80)
    
    class Meta:
        db_table = "hosts"

class Card(models.Model):
    user             = models.ForeignKey('User', on_delete=models.CASCADE)
    country          = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)
    name             = models.CharField(max_length=20)
    card_number      = models.CharField(max_length=400)
    expiration_year  = models.PositiveIntegerField()
    expiration_month = models.PositiveIntegerField()
    zip_code         = models.CharField(max_length=30)
    
    class Meta:
        db_table = "cards"

class Country(models.Model):
    name = models.CharField(max_length=20)
    
    class Meta:
        db_table = "countries"

class Wish(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    room = models.ForeignKey('room.Room', on_delete=models.CASCADE)
    
    class Meta:
        db_table = "wishes"