from django.test import TestCase
from django.utils import timezone
from tickets.models import Ticket
from .models import Cart, CartItem
from django.urls import reverse

class CartModelsTest(TestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(
            event_name = "test_ticket",
            price = 100.00,
            stock = 100,
            date = timezone.now(),
        )
        self.cart = Cart.objects.create(cart_id="test_cart", date_added=timezone.now())
        self.cart_item = CartItem.objects.create(
            ticket=self.ticket,
            cart=self.cart,
            quantity=2,
            active=True
        )
    
    def test_cart_str_method(self):
        self.assertEqual(str(self.cart), "test_cart")

    def test_cart_item_str_method(self):
        expected_str = str(self.ticket.event_name)
        self.assertEqual(str(self.cart_item.ticket.event_name), expected_str)

    def test_subtotal(self):
        expected_sub_total = self.ticket.price * self.cart_item.quantity
        self.assertEqual(self.cart_item.sub_total(), expected_sub_total)



class CartViewTests(TestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(
            event_name = "test_ticket",
            price = 300.00,
            stock = 40,
            date = timezone.now(),
        )
        self.cart = Cart.objects.create(cart_id="test_cart", date_added=timezone.now())
        
    def test_add_cart(self):
        response = self.client.get(reverse('cartapp:add_cart', args=[self.ticket.id]))
        self.assertEqual(response.status_code, 302)

        cart = Cart.objects.get(cart_id=self.client.session.session_key)
        cart_item = CartItem.objects.get(ticket=self.ticket, cart=cart)
        self.assertEqual(cart_item.quantity, 1)


   





