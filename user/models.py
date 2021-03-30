from django.db import models

class User(models.Model):
    first_name    = models.CharField(max_length=30)
    last_name     = models.CharField(max_length=20)
    date_of_birth = models.CharField(max_length=45)
    email         = models.EmailField(max_length=100)
    password      = models.CharField(max_length=300)
    phone_number  = models.CharField(max_length=20)
    image_url     = models.URLField(max_length=3000)
    
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