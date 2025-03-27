from django.shortcuts import redirect, render, get_object_or_404
from tickets.models import Ticket
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if ticket.stock <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect(reverse('ticket_detail', args=[ticket.id]))
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist: 
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    try:
        cart_item = CartItem.objects.get(ticket=ticket, cart=cart)
        if (cart_item.quantity < cart_item.ticket.stock):
            cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(ticket=ticket, quantity=1,cart=cart)
    return redirect('cartapp:cart_detail')

def cart_detail(request, total=0, counter=0, cart_items = None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.ticket.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', 
                    {'cart_items':cart_items, 
                    'total':total, 
                    'counter':counter
                    })

def cart_remove(request, ticket_id):
    cart= Cart.objects.get(cart_id=_cart_id(request))
    ticket = get_object_or_404(Ticket, id=ticket_id)
    cart_item = CartItem.objects.get(ticket=ticket, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cartapp:cart_detail')

def full_remove(request, ticket_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    ticket = get_object_or_404(Ticket, id=ticket_id)
    cart_item = CartItem.objects.get(ticket=ticket, cart=cart)
    cart_item.delete()
    return redirect('cartapp:cart_detail')
