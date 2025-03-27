from django.urls import path
from . import views
from .views import add_ticket, TicketPageView, delete_ticket, EventTypePageView, EventsByEventTypeView, TicketsByEventView, TicketDetailView

urlpatterns = [
    path('add/', add_ticket, name='add_ticket'),
    path('tickets/', TicketPageView.as_view(), name='ticket_list'),
    path('delete/<int:ticket_id>/', delete_ticket, name='delete_ticket'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('eventtype/', EventTypePageView.as_view(), name='eventtype_list'),
    path('events/<uuid:pk>/', EventsByEventTypeView.as_view(), name='events_by_eventtype'),
    path('tickets-by-event/<uuid:pk>/',TicketsByEventView.as_view(),name='tickets_by_event'),
    path('ticket/<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
]
