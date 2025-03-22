from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, Event, EventType
from django.views import View
from django.views.generic import ListView, DetailView



    
def home(request):
    return render(request, 'home.html')

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

def tickets(request):
    tickets = Ticket.objects.all()
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})


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