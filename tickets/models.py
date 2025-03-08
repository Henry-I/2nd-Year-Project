from django.db import models

# Create your models here.
class Ticket(models.Model):
    event = models.ForeignKey() # no events app yet
    seat_type = models.CharField(max_length=100)
    ticket_type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.event_name} - {self.seat_type}"
