from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .owner import OwnerCreateView, OwnerDeleteView, OwnerDetailView, OwnerListView, OwnerUpdateView
from .models import Roadmap, Topic, Item, Unit

# Create your views here.
class HomeView(ListView):
    """
    Pasa un queryset que son los últimos 3 tracks que se hicieron y otro que son todos los topics.
    """
    model = Topic
    fields = '__all__'
    template_name = 'roadmaps/main.html'
    
    # Le agrego al context que se pasa a la template el queryset tambén de Roadmaps
    # https://docs.djangoproject.com/en/3.0/topics/class-based-views/generic-display/#adding-extra-context
    def get_context_data(self, **kwargs):
        # obtenemos el contexto que iba a ser originalmente pasado a nuestra template
        context = super().get_context_data(**kwargs)
        # agregamos el queryset de roadmaps filtrado
        # https://docs.djangoproject.com/en/3.0/topics/db/queries/#limiting-querysets
        context['roadmap_list'] = Roadmap.objects.order_by('created_at')[0:4]
        return context

class RoadmapListView(ListView):
    model = Roadmap
    fields ='__all__'

class RoadmapDetailView(DetailView):
    model = Roadmap
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unit_list']= Unit.objects.filter(roadmap_id=self.kwargs['pk'])
        return context
        

class UnitDetailView(DetailView):
    model = Unit
    fields = '__all__'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rid = Unit.objects.filter(id=self.kwargs['pk'])[0].roadmap_id
        qs1 = Unit.objects.filter(roadmap_id=rid)
        qs2 = qs1.order_by('place')
        context['unit_list'] = qs2
        context['item_list'] = Item.objects.filter(unit_id=self.kwargs['pk'])
        return context