from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.utils import timezone

class Topic(models.Model):
    title = models.CharField(
        null=False,
        max_length=30,
        validators=[MinLengthValidator(2, 'Title must be greater than 2 characters')],
        default='Title',
    )
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True) # Mantenemos ésto para anunciar con un listón cuando un topic sea nuevo
    
    # Método decorado para indicar que es nuevo
    @property
    def is_topic_new(self):
        return (timezone.now() - self.created_at).days < 7

    def __str__(self):
        return self.title

class Roadmap(models.Model):
    parent_roadmap = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="children_roadmaps"
    )
    place = models.IntegerField(null=True, blank=True)
    topic = models.ManyToManyField(Topic, related_name='roadmaps')
    roadmap_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='roadmaps',
        through='RoadmapMembership',
    )
    title = models.CharField(
        null=False,
        max_length=50,
        validators=[MinLengthValidator(2, 'Title must be greater than 2 characters')],
        default='Title',
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, # El primer argumento de éste método es el modelo al cual apuntamos (EN ÉSTE CASO, LATABLA USER QUE NOS HACE DJANGO)
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to='roadmap_images', blank=True, null=True)

    objectives = models.CharField(max_length=1200, default='')
    
    methods_and_resources = models.CharField(max_length=250, default='')

    estimated_time = models.CharField(max_length=100, default='')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def model_name(self):
        return self._meta.model_name
    
    def __str__(self):
        if self.place != None:
            return "Unit " + str(self.place) +" | " + self.title
        return self.title

class Unit(models.Model):
    roadmap = models.ForeignKey(
        Roadmap,
        on_delete=models.CASCADE, # Si se borran los roadmap, se borran las units
        blank=True, # Un roadmap puede no indicar nada en el lugar de las units
        null=True, # Un roadmap puede no tener ninguna unit
        related_name="units" # Como se llama la columna de las Unit en la tabla Roadmap
    )
    unit_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='units',
        through='UnitMembership',
    )
    title = models.CharField(
        null=False,
        max_length=50,
        validators=[MinLengthValidator(2, 'Title must be greater than 2 characters')],
        default='Title',
    )
    # Campo para indicar el orden
    place = models.IntegerField(null=False, default=1)
    objectives = models.CharField(max_length=1200, default='')

    def model_name(self):
        return self._meta.model_name

    def __str__(self):
        return "Unit " + str(self.place) +" | " + self.title


class Item(models.Model):
    parent_item = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="children_items"
    )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    item_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='items',
        through='ItemMembership',
    )
    title = models.CharField(
        null=False,
        max_length=50,
        validators=[MinLengthValidator(2, 'Title must be greater than 2 characters')],
        default='Title',
    )
    # Campo para indicar el orden
    place = models.IntegerField(null=False, default=1)
    objectives = models.CharField(max_length=1200, default='')
    link = models.URLField(
        max_length=128, 
        db_index=True, 
        unique=False, 
        blank=True
    )

    def __str__(self):
        return self.title


    
# Tabla Joint de Miembros    
class RoadmapMembership(models.Model):

    """Creamos ésta clase, porque no le queremos delegar ésta tabla a Python así le podemos agregar nosotros los campos created_at y updated_at para saber el
    orden cronológico en el que el usuario se enlistó a sus cursos"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False) # Si checkeamos la box o no
    created_at = models.DateTimeField(auto_now_add=True) # Cuando se creó la membresía (fila de ésta tabla)
    updated_at = models.DateTimeField(auto_now=True) # Cuando se modíficó la membresía

    def __str__(self):
        return "User: " + str(self.user.username) + " | " + "Course: " + str(self.roadmap.title     )
    
class UnitMembership(models.Model):

    """Creamos ésta clase, porque no le queremos delegar ésta tabla a Python así le podemos agregar nosotros los campos created_at y updated_at para saber el
    orden cronológico en el que el usuario se enlistó a sus cursos"""

    roadmap_membership = models.ForeignKey(RoadmapMembership, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False) # Si checkeamos la box o no
    created_at = models.DateTimeField(auto_now_add=True) # Cuando se creó la membresía (fila de ésta tabla)
    updated_at = models.DateTimeField(auto_now=True) # Cuando se modíficó la membresía

    def __str__(self):
        return "User: " + str(self.user.id) + " | " + "Course: " + str(self.unit.id)

class ItemMembership(models.Model):

    """Creamos ésta clase, porque no le queremos delegar ésta tabla a Python así le podemos agregar nosotros los campos created_at y updated_at para saber el
    orden cronológico en el que el usuario se enlistó a sus cursos. Además le agregamos el campo unit_membership y el campo roadmap_membership que son llenados
    automáticamente por las views, éste nos va a servir para verificar las memberships superiores y además linkear el done y el undone"""


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    unit_membership = models.ForeignKey(UnitMembership, on_delete=models.CASCADE) # Éste campo linkea a la membership de éste item con le membership de su unit padre, para mas tarde sombrear todas las units cuyos items estén terminados
    parent_item_membership = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="children_item_memberships"
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False) # Si checkeamos la box o no
    created_at = models.DateTimeField(auto_now_add=True) # Cuando se creó la membresía (fila de ésta tabla)
    updated_at = models.DateTimeField(auto_now=True) # Cuando se modíficó la membresía

    def __str__(self):
        return "User: " + str(self.user.username) + " in " + "Course: " + str(self.item.title)