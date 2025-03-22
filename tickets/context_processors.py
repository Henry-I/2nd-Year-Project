from .models import EventType, Event, Ticket

def eventtype_list(request):
    return {'eventtype_list': EventType.objects.all()}

def event_list(request):
    return {'event_list': Event.objects.all()}

