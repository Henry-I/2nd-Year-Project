from tickets.models import Ticket
from django.views.generic import ListView
from django.db.models import Q

class SearchResultsListView(ListView):
    model = Ticket
    context_object_name = 'ticket_list'
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Ticket.objects.filter(Q(event_name__icontains=query) | Q(event__name__icontains=query))

    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context




