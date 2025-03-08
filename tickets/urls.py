from django.urls import path
from . import views
from .views import add_ticket, tickets, delete_ticket

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', add_ticket, name='add_ticket'),
    path('tickets/', tickets, name='ticket_list'),
    path('delete/<int:ticket_id>/', delete_ticket, name='delete_ticket'),
]
