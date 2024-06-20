from django.shortcuts import render
from markets.models import *
from django.views import generic


# Create your views here.
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_markets = Markets.objects.all().count()

    context = {
        'num_markets': num_markets
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'markets/index.html', context=context)


class MarketsListView(generic.ListView):
    model = Markets
    paginate_by = 20
    template_name = 'markets/markets_list.html'

    def get_queryset(self):
        order = self.request.GET.get('sort_by')
        if order is None or order == '':
            order = 'pk'
        match self.request.GET.get('find_by'):
            case "zip":
                return Markets.objects.filter(zip__icontains=self.request.GET.get('q')).order_by(order)
            case "state":
                return Markets.objects.filter(state__icontains=self.request.GET.get('q')).order_by(order)
            case "city":
                return Markets.objects.filter(city__icontains=self.request.GET.get('q')).order_by(order)
            case _:
                return Markets.objects.all().order_by(order)

    # def sort(self):
    #     match self.request.GET.get('sort_by'):
    #         case "city": markets.objects.order_by("city")
    #         case "-city": markets.objects.order_by("-city")
    #         case "state": markets.objects.order_by("state")
    #         case "-state": markets.objects.order_by("-state")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        context['find_by'] = self.request.GET.get('find_by')
        return context


class MarketsDetailView(generic.DetailView):
    model = Markets
    template_name = 'markets/markets_detail.html'
