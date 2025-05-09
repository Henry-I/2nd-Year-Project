from django.shortcuts import redirect, render, get_object_or_404, reverse
from tickets.models import Ticket, BookingDetails
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import stripe
from order.models import Order, OrderItem
from stripe import StripeError
from vouchers.models import Voucher
from vouchers.forms import VoucherApplyForm
from decimal import Decimal


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
    discount = 0
    voucher_id = 0
    new_total = 0
    voucher = None
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.ticket.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)  # Convert total to cents
    description = 'Online Shop - New Order'
    voucher_apply_form = VoucherApplyForm()

    try:
        voucher_id = request.session.get('voucher_id')
        voucher = Voucher.objects.get(id=voucher_id)
        if voucher != None:
            discount = (total*(voucher.discount/Decimal('100')))
            new_total = (total - discount)
            stripe_total = int(new_total * 100)
    except:
        ObjectDoesNotExist
        pass

    if request.method == 'POST':
        try:
            # Create a new Stripe Checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': 'Order from Perfect Cushion Shop',
                        },
                        'unit_amount': stripe_total,
                    },
                    'quantity': 1,
                }],
                mode='payment',
 		   billing_address_collection='required', 
                shipping_address_collection={},
                payment_intent_data={'description': description},
                success_url=request.build_absolute_uri(reverse('cartapp:new_order'))+ f"?session_id={{CHECKOUT_SESSION_ID}}&voucher_id={voucher_id}&cart_total={total}",
                cancel_url=request.build_absolute_uri(reverse('cartapp:cart_detail')),    
            )
            # Redirect to Stripe Checkout
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            # Render the template with an error message
            return render(request, 'cart.html', {
                'cart_items': cart_items,
                'total': total,
                'counter': counter,
                'error': str(e),  # Display error if there's an issue with Stripe
            })
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'counter': counter,
        'voucher_apply_form': voucher_apply_form,
        'new_total': new_total,
        'voucher': voucher,
        'discount': discount,

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

def empty_cart(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        cart_items.delete()  
        cart.delete()
        return redirect('ticket_list')
    except Cart.DoesNotExist:
        pass
    return redirect('cartapp:cart_detail')

def create_order(request):
    try:
        session_id = request.GET.get('session_id')
        cart_total = request.GET.get('cart_total')
        voucher_id = request.GET.get('voucher_id')

        if not session_id:
            raise ValueError("Session ID not found.")

        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except StripeError as e:
            return redirect("ticket_list") 

        customer_details = session.customer_details
        if not customer_details or not customer_details.address:
            raise ValueError("Missing information in the Stripe session.")

        billing_address = customer_details.address
        billing_name = customer_details.name
        shipping_address = customer_details.address
        shipping_name = customer_details.name

        try:
            order_details = Order.objects.create(
                token=session.id,
                total=session.amount_total / 100,  
                emailAddress=customer_details.email,
                billingName=billing_name,
                billingAddress1=billing_address.line1,
                billingCity=billing_address.city,
                billingPostcode=billing_address.postal_code,
                billingCountry=billing_address.country,
                shippingName=shipping_name,
                shippingAddress1=shipping_address.line1, 
                shippingCity=shipping_address.city, 
                shippingPostcode=shipping_address.postal_code,
                shippingCountry=shipping_address.country,
            )
            order_details.save()
        except Exception as e: 
            print(f"Error: {e}")
            return redirect("ticket_list") 

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, active=True)
        except ObjectDoesNotExist:
            return redirect("ticket_list")  
        except Exception as e:
            print(f"Error: {e}")
            return redirect("ticket_list") 

        voucher = get_object_or_404(Voucher, id=voucher_id)
        if voucher != None:
            order_details.voucher = voucher
            cart_total = Decimal(cart_total)
            order_details.discount = cart_total*(voucher.discount/Decimal('100'))
            order_details.total = (cart_total-order_details.discount)
            order_details.save()
 

        for item in cart_items:
            try:
                oi = OrderItem.objects.create(
                    product=item.ticket.event_name,
                    quantity=item.quantity,
                    price=item.ticket.price,
                    order=order_details
                )
                oi.save()
                '''Reduce stock when order is placed or saved'''
                ticket = Ticket.objects.get(id=item.ticket.id)
                ticket.stock = int(item.ticket.stock - item.quantity)
                ticket.save()
                if voucher != None:
                    discount = (oi.price*(voucher.discount/Decimal('100')))
                    oi.price = (oi.price - discount)
                else:
                    oi.price = oi.price*oi.quantity
                oi.save()

                empty_cart(request)
            except Exception as e:
                return redirect("ticket_list")  
        return redirect('order:thanks', order_id=order_details.id)

    except ValueError as ve:
        print(f"Error: {ve}")
        return redirect("ticket_list")  

    except StripeError as se:
        print(f"Stripe Error: {se}")
        return redirect("ticket_list") 

    except Exception as e:
        print(f"Unexpected error: {e}")
        return redirect("ticket_list") 

