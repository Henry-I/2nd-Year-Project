from django.shortcuts import render
from tickets.models import ticket

# Create your views here.


def CartAdd(request, ticket_id):
    