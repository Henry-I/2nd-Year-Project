from django import forms
from .models import Ticket, BookingDetails

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event_name', 'price', 'date']

class BookingDetailsForm(forms.ModelForm):
    class Meta:
        model= BookingDetails
        fields= ['f_name','l_name','email','phone','ticket_type','row','seat']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name in self.fields:
                self.fields[field_name].required = True