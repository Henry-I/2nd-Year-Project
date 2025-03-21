from django.urls import path
from . import views
from .views import add_ticket, tickets, delete_ticket, EventTypePageView, EventsByEventTypeView

urlpatterns = [
    path('add/', add_ticket, name='add_ticket'),
    path('tickets/', tickets, name='ticket_list'),
    path('delete/<int:ticket_id>/', delete_ticket, name='delete_ticket'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('eventtype/', EventTypePageView.as_view(), name='eventtype_list'),
    path('events/<uuid:pk>/', EventsByEventTypeView.as_view(), name='events_by_eventtype'),
]
