from django.views.generic import ListView, TemplateView, DetailView
from .models import  Item


class ItemListView(ListView):

    model = Item
    template_name = 'item_list.html'

    def get_context_data(self, **kwargs):
        product_list = Item.objects.all()
        context = super().get_context_data( **kwargs)
        context['products'] = product_list
        return context

class IndexView(TemplateView):
    template_name = 'index.html'