from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

class OwnerListView(LoginRequiredMixin, ListView):
    """
    Sub-clase de ListView que además de pasarle el request al form, te pide unlogin antes de ver la ListView
    """

class OwnerDetailView(LoginRequiredMixin, DetailView):
    """
    Sub-clase de ListView que además de pasarle el request al form,te pide que estés logueado antes de ver la DetailView
    """

class OwnerCreateView(LoginRequiredMixin, CreateView):
    """
    Sub-clase de CreateView que se asegura de que User esté logueado antes de poder llegar a ésta view y que pasa a User como owner.
    """

    def form_valid(self, form):
        print('form_valid called')
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super(OwnerCreateView, self).form_valid(form)

class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    """
    Sub-clase de UpdateView que pasa el request al form de la template y limita el queryset que puede generar el form a User.
    """

    def get_queryset(self):
        print('update get_queryset called')
        """ Limitamos el usuario a solo poder editar sus propios datos. """
        qs = super(OwnerUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    """
    Sub-clase the DeleteView que no le permite a borrar los datos de otros usuarios
    """

    def get_queryset(self):
        print('delete get_queryset called')
        qs = super(OwnerDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)