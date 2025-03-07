from django.shortcuts import render, get_object_or_404
from django.views import view

# Create your views here.

class BuyTicketView(View):
    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)

        return render()
    
