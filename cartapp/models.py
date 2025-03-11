from django.db import models
from tickets.models import ticket

# Create your models here.

class Cart(models.Model):
    cart_ID = models.CharField(max_length=255)
    date = models.DateField(auto_add_now=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    ticket = models.ForeignKey(ticket on_delete=Models.CASCADE)
    cart = models.ForeignKey(Cart on_delete=Models.CASCADE)
    quantity = models.IntegerField()
    
    def subtotal(self):
        return ticket.price * self.quantity

    def __str__(self):
        return self.name
        
