from django.db import models

class Convenience(models.Model):
    name = models.CharField(max_length=45)
    
    class Meta:
        db_table = "conveniences"

class Rule(models.Model):
    name = models.CharField(max_length=45)
    
    class Meta:
        db_table = "rules"

class RoomRule(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    rule = models.ForeignKey('Rule', on_delete=models.CASCADE)
    
    class Meta:
        db_table = "room_rules"

class RoomConvenience(models.Model):
    room        = models.ForeignKey('Room', on_delete=models.CASCADE)
    convenience = models.ForeignKey('Convenience', on_delete=models.CASCADE)
    
    class Meta:
        db_table = "room_conveniences"

class Type(models.Model):
    name        = models.CharField(max_length=20)
    description = models.CharField(max_length=60)
    
    class Meta:
        db_table = "types"

class CheckinType(models.Model):
    name        = models.CharField(max_length=20)
    description = models.CharField(max_length=60)
    
    class Meta:
        db_table = "checkin_types"

class City(models.Model):
    name = models.CharField(max_length=20)
    
    class Meta:
        db_table = "cities"

class District(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    
    class Meta:
        db_table = "districts"

class AddressLine(models.Model):
    city     = models.ForeignKey('City', on_delete=models.CASCADE)
    district = models.ForeignKey('District', on_delete=models.CASCADE)
    name     = models.CharField(max_length=20)    
    
    class Meta:
        db_table = "address_lines"

class Room(models.Model):
    title             = models.CharField(max_length=500)
    type              = models.ForeignKey('Type', on_delete=models.CASCADE)
    host              = models.ForeignKey('user.Host', on_delete=models.CASCADE)
    checkin           = models.ForeignKey('CheckinType', on_delete=models.CASCADE)
    city              = models.ForeignKey('City', on_delete=models.CASCADE)
    district          = models.ForeignKey('District', on_delete=models.CASCADE)
    address_line      = models.ForeignKey('AddressLine', on_delete=models.CASCADE)
    detail_address    = models.CharField(max_length=45)
    zip_code          = models.CharField(max_length=20)
    description       = models.TextField()
    price             = models.DecimalField(max_digits= 10, decimal_places= 2)    
    discount_rate     = models.DecimalField(max_digits= 3, decimal_places= 2, default=0)
    latitude          = models.DecimalField(max_digits= 11, decimal_places= 8)
    longitude         = models.DecimalField(max_digits= 11, decimal_places= 8)
    maximum_people    = models.PositiveIntegerField()    
    checkin_time      = models.TimeField()
    checkout_time     = models.TimeField()
    bedroom           = models.PositiveIntegerField()
    bathroom          = models.PositiveIntegerField()
    bed               = models.PositiveIntegerField()
    room_conveniences = models.ManyToManyField(
        'Convenience',
        through        = 'RoomConvenience',
        through_fields = ('room', 'convenience'),
        related_name   = 'convenience_rooms',
    )
    room_rules        = models.ManyToManyField(
        'Rule',
        through        = 'RoomRule',
        through_fields = ('room', 'rule'),
        related_name   = 'rule_rooms',
    )
    reviews           = models.ManyToManyField(
        'user.User',
        through        = 'Review',
        through_fields = ('room', 'user'),
        related_name   = 'reviewed_room',
    )
    booked_people     = models.ManyToManyField(
        'user.User',
        through        = 'book.Book',
        through_fields = ('room', 'user'),
        related_name   = 'booked_rooms',
    )
    wished_people     = models.ManyToManyField(
        'user.User',
        through        = 'user.Wish',
        through_fields = ('room', 'user'),
        related_name   = 'wished_rooms',
    )
        
    class Meta:
        db_table = "rooms"

class Image(models.Model):
    room      = models.ForeignKey('Room', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=3000)    
    
    class Meta:
        db_table = "images"

class Review(models.Model):
    user          = models.ForeignKey('user.User', on_delete=models.CASCADE)
    room          = models.ForeignKey('Room', on_delete=models.CASCADE)
    content       = models.CharField(max_length=45)
    created_at    = models.DateTimeField(auto_now_add=True)
    cleanliness   = models.PositiveIntegerField()
    accuracy      = models.PositiveIntegerField()
    communication = models.PositiveIntegerField()
    location      = models.PositiveIntegerField()
    checkin       = models.PositiveIntegerField()
    satisfaction  = models.PositiveIntegerField()
    
    class Meta:
        db_table = "reviews"