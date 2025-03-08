from django.db import models

# Create your models here.
class Event(models.Model):
    event_name = models.CharField(max_legnth=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank = True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.event_name
    

class EventType(models.Model):
    name = models.CharField(max_length=100)
    description = models.Text(blank = True)

    def __str__(self):
        return self.name

