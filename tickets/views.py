from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, Event, EventType
from django.views import View
from django.views.generic import ListView, DetailView
from .forms import BookingDetailsForm
from order.models import Order


class TicketDetailView(DetailView):
    model = Ticket
    template_name = 'ticket_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = None
        if self.request.user.is_authenticated:
                order = Order.objects.filter(emailAddress=self.request.user.email).first()  
        context['order'] = order
        return context

def home(request):
    tickets = Ticket.objects.all()[:5]
    return render(request, 'home.html', {'tickets': tickets})


def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

class BuyTicketView(View):
    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)

        return render()

def add_ticket(request):
    return render(request, 'tickets/add_ticket.html')

class TicketPageView(ListView):
    model = Ticket
    template_name = 'tickets.html'  
    context_object_name = 'ticket_list'
    paginate_by = 4

def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == "POST":
        ticket.delete()
        return redirect('ticket_list')
    return render(request, 'tickets/delete_ticket.html', {'ticket': ticket})

class EventTypePageView(ListView):
    model = EventType
    context_object_name = 'eventtype_list'

class EventsByEventTypeView(DetailView):
    model = EventType
    template_name = 'events_by_eventtype.html'
    context_object_name = 'eventtype'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_type = self.object
        events = Event.objects.filter(event_type=event_type)
        context['events'] = events
        return context

class TicketsByEventView(DetailView):
    model = Event
    template_name = 'tickets_by_event.html'
    context_object_name = 'event'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        tickets = Ticket.objects.filter(event=event)
        context['tickets'] = tickets
        return context

def ticket_checkout(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        form = BookingDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cartapp:add_cart', ticket_id=ticket.id)
        else:
            return render(request, 'ticket_checkout.html', {'form': form, 'ticket': ticket})
    
    else:
        form = BookingDetailsForm()

    return render(request, 'ticket_checkout.html', {'form': form, 'ticket': ticket})
