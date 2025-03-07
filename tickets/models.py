from django.db import models

# Create your models here.

class Ticket(models.Model):
    event = models.ForeignKey() # no events app yet
    ticket_type = models.CharField(max_length=100)
    seat_type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return 

    