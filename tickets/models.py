from django.db import models
import uuid

# Create your models here.
class EventType(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250, unique=True)
    
    def __str__(self):
        return self.name

class Event(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to='Event', blank=True)
    event_type = models.ManyToManyField(EventType)
    
    
    def __str__(self):
        return self.name
        

class Ticket(models.Model):
    event_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='Tickets', blank=True)
    event = models.ManyToManyField(Event)
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    
    def __str__(self):
        return self.event_name
