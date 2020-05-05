from django import forms
from itertools import chain
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, View, TemplateView
from .owner import OwnerCreateView, OwnerDeleteView, OwnerDetailView, OwnerListView, OwnerUpdateView
from .models import Roadmap, Topic, Item, Unit, RoadmapMembership, UnitMembership, ItemMembership

# Create your views here.
class RedirectView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('account', pk=request.user.id)
        else:
            return redirect('main')



class MainView(View):
    """
    Pasa un queryset que son los últimos 3 tracks que se hicieron y otro que son todos los topics.
    """

    def get(self, request):      
        context = {}
        template_name = 'roadmaps/main.html'
        context['topic_list'] = Topic.objects.order_by('created_at') # https://docs.djangoproject.com/en/3.0/topics/class-based-views/generic-display/#adding-extra-context
        context['roadmap_list'] = Roadmap.objects.order_by('created_at')[0:4] # https://docs.djangoproject.com/en/3.0/topics/db/queries/#limiting-querysets
        return render(request, template_name, context)

class RoadmapListView(ListView):
    model = Roadmap
    fields ='__all__'

class RoadmapDetailView(DetailView):
    model = Roadmap
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #Agregamos ésto para ver qué roadmap fué el último visitado por el dueño de la session
        last_seen = self.request.session.get('last_seen', Roadmap.objects.filter(id=self.kwargs['pk'])) #Creamos un last_seen si no lo hay
        request.session['last_seen'] = Roadmap.objects.filter(id=self.kwargs['pk']) #Modificamos el last_seen por el que el user está viendo ahora si lo hay
        
        #Pasamos un queryset que sea mezcla de Units y Roadmaps
        unit_results = Unit.objects.filter(roadmap_id=self.kwargs['pk'])
        roadmap_results = Roadmap.objects.filter(parent_roadmap=self.kwargs['pk'])
        # Combinamos los querysets
        queryset_chain = chain(
            unit_results,
            roadmap_results
        )
        qs = sorted(
            queryset_chain,
            key=lambda instance: instance.place,
            reverse=False #Cambiar ésto según el órden que quiero
        )
        self.count = len(qs)
        context['unit_list']= qs

        #Si el usuario ni inició sesión, lo mandamos a logearse (por ahora dejamos ese mensaje que en algún momento se mostrará en una alert amarilla de Bootstrap)
        if not self.request.user.is_authenticated:
            context['start_roadmap_message'] = 'You are not logged in, log in so you can join this roadmap' #Mensaje perosnalizado para la alert de Bootstrap
        
        rm = context['roadmap'] #El roadmap actual (el de nuestra view)
        condition = rm.parent_roadmap
        while condition:
            if rm.parent_roadmap==None:
                break
            try:
                RoadmapMembership.objects.get(user=self.request.user.id, roadmap=rm.id)
                #La línea de arriba debería crashear antes de leer las líneas de abajo
                rm = context['roadmap']
                new_membership = RoadmapMembership(user=self.request.user, roadmap=rm)
                condition = False  #Si se encuentra una membresía padre, dejamos de buscar. Le indicamos al while loop que deje de buscar cambiando la condición a False
            except RoadmapMembership.DoesNotExist:
                rm = rm.parent_roadmap

        if not (condition == False): #Si condition == False significa que condition no es None, entonces la única forma de que condition sea False es que se haya activado porque el loop encontró una memberhip padre
            context['start_roadmap_message'] = 'You\re not a member of this roadmap, join it to see it\'s content'
        
        return context



class UnitDetailView(DetailView):
    model = Unit
    fields = '__all__'
    def get_context_data(self, **kwargs):

        #Funcionalidad last seem
        last_seen = self.request.session.get('last_seen', Unit.objects.filter(id=self.kwargs['pk'])) #Creamos un last_seen si no lo hay
        request.session['last_seen'] =  Unit.objects.filter(id=self.kwargs['pk']) #Modificamos el last_seen por el que el user está viendo ahora si ya hay un last_seen

        # Separo al context para agregarle lo que quiera
        context = super().get_context_data(**kwargs)
        # Le agrego al context dos querysets ordenados 
        rid = Unit.objects.filter(id=self.kwargs['pk'])[0].roadmap_id
        qs1 = Unit.objects.filter(roadmap_id=rid)
        qs1 = qs1.order_by('place')
        context['unit_list'] = qs1 # Queryset para la columna derecha de la template
        qs2 = Item.objects.filter(unit_id=self.kwargs['pk'], parent_item=None)
        qs2 = qs2.order_by('place')
        context['item_list'] = qs2 # Queryset para la columna izquierda de la template
        
        if not self.request.user.is_authenticated:
            context['start_roadmap_message'] = 'You are not logged in, log in so you can join this roadmap' #Mensaje perosnalizado para la alert de Bootstrap
        
        
        else: #Redundante preguntar si el usuario está logueado
            #Obtenemos el roadmap padre en dos pasos
            context_unit = context['unit'] #Obtenemos la variable unit que genera nuestra generic DeatilView y la pasa en el context
            parent_roadmap = context_unit.roadmap
            
            #Ya con el roadmap padre, nos fijamos si existe una membersía que tenga al roadmap padre y al user del request
            try:
                parent_roadmap_membership = RoadmapMembership.objects.get(roadmap=parent_roadmap.id, user=self.request.user.id)
                
                # Si todo sale bien y entonces ya existe la membership (parent_roadmap_membership), el user ya joineó el roadmap y no queda mas que verificar si joineo las units.
                try:
                    this_unit_membership = UnitMembership.objects.get(unit=context_unit, user=self.request.user.id, roadmap_membership=parent_roadmap_membership.id)

                #Si el usuario está inscripto en el roadmap padre, pero no está inscripto en la unit, entonces no queda mas que crear la membership para esa unit
                except UnitMembership.DoesNotExist:
                    new_unit_membership = UnitMembership(unit=context_unit, user=self.request.user, roadmap_membership=parent_roadmap_membership)
                    new_unit_membership.save()

                # Crear una membership para cada item de la unit
                items_qs = Item.objects.all().filter(unit_id=self.kwargs['pk']) #Obtenemos el queryset con todos los ítems que pertenezcana ésta unit (y sin importar la jerarquía, todos están sujetos a la misma unit desde su creación)
                this_unit_membership = UnitMembership.objects.all().filter(unit=context_unit, user=self.request.user, roadmap_membership=parent_roadmap_membership).first() #Obtenemos la membresía de ésta unit, que va a ser el común denominador entre todas las ItemMembership que vamos a crear
                for item in items_qs:
                    try:
                        this_item_membership = ItemMembership.objects.get(
                            user=self.request.user.id,
                            unit_membership=this_unit_membership.id,
                            item=item.id
                        )

                    except ItemMembership.DoesNotExist:
                        if item.parent_item:
                            print('This item has a parent')
                            this_item_parent_item_membership = ItemMembership.objects.get(
                                user=self.request.user.id,
                                unit_membership=this_unit_membership.id,
                                item = item.parent_item,                                
                            )
                            this_item_membership = ItemMembership(
                                user=self.request.user,
                                unit_membership=this_unit_membership,
                                parent_item_membership=this_item_parent_item_membership,
                                item=item,
                            )
                            this_item_membership.save()
                        else:
                            print('This item has not a parent')
                            this_item_membership = ItemMembership(user=self.request.user, item=item, unit_membership=this_unit_membership)
                            this_item_membership.save()

                #Pasamos la lista de item_memberships sin padres para que procese la template                
                context['item_membership_list'] = ItemMembership.objects.all().filter(unit_membership=this_unit_membership,user=self.request.user, parent_item_membership=None).order_by('item__place') #Obtenemos las mebresisas de todos los ítems de la unidad en cuestión y del user en cuestión. Además no pueden tener padres, así creamos nuestra tree view recursiva
            
            except RoadmapMembership.DoesNotExist:
                context['start_roadmap_message'] = 'You\re not a member of this roadmap, join it to see it\'s content'

        return context

class JoinRoadmapView(View):
    def post(self, request, *args, **kwargs):
        rm = Roadmap.objects.get(id=self.kwargs['pk'])
        new_roadmap_member = RoadmapMembership(user=self.request.user, roadmap=rm)
        new_roadmap_member.save()
        return redirect('roadmap_detail', pk=rm.id)

def tree_finished(item_membership, value):
    item_membership.finished = value
    item_membership.save()
    if item_membership.children_item_memberships:
        for child_item_membership in item_membership.children_item_memberships.all():
            tree_finished(child_item_membership, value)


class TickCheckbox(View):
    def post(self, request, *args, **kwargs):
        item_membership = ItemMembership.objects.all().filter(id=self.kwargs['pk']).first()
        if item_membership.finished == False:
            tree_finished(item_membership, True)
            print('This item is finished!')
            
        else:
            item_membership.finished = False
            item_membership.save()

        return redirect('unit_detail', pk=item_membership.item.unit.id)


