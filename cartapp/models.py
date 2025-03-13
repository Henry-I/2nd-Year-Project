from django.db import models
from tickets.models import Ticket

# Create your models here.

class Cart(models.Model):
    cart_ID = models.CharField(max_length=255)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    def subtotal(self):
        return ticket.price * self.quantity

    def __str__(self):
        return self.name
        
