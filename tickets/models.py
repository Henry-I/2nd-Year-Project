from django.db import models

# Create your models here.
class Ticket(models.Model):
    event_name = models.CharField(max_length=255)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, default=1)
    seat_type = models.CharField(max_length=100)
    ticket_type = models.CharField(max_length=100, default='Regular')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    date = models.DateField()

    def __str__(self):
        return f"{self.event_name} - {self.seat_type}"
    
class Event(models.Model):
    name = models.CharField(max_length=100)
