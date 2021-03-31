from django.db import models

class BookStatus(models.Model):
    name          = models.CharField(max_length=30)
    
    class Meta:
        db_table = "book_status"

class Book(models.Model):
    room             = models.ForeignKey('room.Room', on_delete=models.CASCADE)
    user             = models.ForeignKey('user.User', on_delete=models.CASCADE)
    book_status      = models.ForeignKey('BookStatus', on_delete=models.SET_NULL, null=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    number_of_guests = models.PositiveIntegerField()
    message          = models.CharField(max_length=45, null=True)
    start_date       = models.DateTimeField()
    end_date         = models.DateTimeField()
    serial_number    = models.CharField(max_length=45)
    
    class Meta:
        db_table = "books"

