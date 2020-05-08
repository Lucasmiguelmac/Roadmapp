from .signals import object_viewed_signal

class ObjectViewMixin:
    #Cómo en views.py trabajamos con class-based views, lo que vamos a sobrescribir es el método dispatch que tienen las class-based views
    def dispatch(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except self.model.DoesNotExist:
            instance = None
        if request.user.is_authenticated and instance is not None:
            object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return super(ObjectViewMixin, self).dispatch(request, *args, **kwargs)