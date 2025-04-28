from django.contrib import admin
from .models import Ticket, Event, EventType, BookingDetails

class TicketAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'price', 'stock', 'description']     
    search_fields = ['event_name']

class BookingDetailsAdmin(admin.ModelAdmin):
    list_display = ['l_name','f_name','email','phone','ticket_type','row','seat']
    list_display_links = ('l_name','f_name')


# Register your models here.
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Event)
admin.site.register(EventType)
admin.site.register(BookingDetails, BookingDetailsAdmin)
 