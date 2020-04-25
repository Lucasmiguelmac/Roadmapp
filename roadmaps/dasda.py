from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.utils import timezone


class Item(models.Model):
    item_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='items',
        through='ItemMembership',
    )
    title = models.CharField(
        null=False,
        max_length=30,
        validators=[MinLengthValidator(2, 'Title must be greater than 2 characters')]
    )
    # Campo para indicar el orden
    place = models.IntegerField(null=False, default=1)
    objectives = models.TextField()
    link = models.TextField(null=True)

    def __str__(self):
        return self.title


class Unit(models.Model):
    unit_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='units',
        through='UnitMembership',
    )
    name = models.CharField(
        null=False,
        max_length=30,
        validators=[MinLengthValidator(2, 'Title must be greater than 2 characters')]
    )
    # Campo para indicar el orden
    place = models.IntegerField(null=False, default=1)
    about = models.TextField()
    items = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return "Unit " + str(self.place) +": " + self.name


class Roadmap(models.Model):
    roadmap_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='roadmaps',
        through='RoadmapMembership',
    )
    title = models.CharField(
        null=False,
        max_length=30,
        validators=[MinLengthValidator(2, 'Title must be greater than 2 characters')]
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, # El primer argumento de éste método es el modelo al cual apuntamos (EN ÉSTE CASO, LATABLA USER QUE NOS HACE DJANGO)
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to='roadmap_images', blank=True)

    objectives = models.CharField(max_length=1200, default='')

    units = models.ForeignKey(Unit, on_delete=models.CASCADE)
    
    methods_and_resources = models.CharField(max_length=250, default='')

    estimated_time = models.CharField(max_length=100, default='')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Topic(models.Model):
    title = models.CharField(
        null=False,
        max_length=30,
        validators=[MinLengthValidator(2, 'Title must be greater tahn 2 characters')]
    )
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True) # Mantenemos ésto para anunciar con un listón cuando un topic sea nuevo
    roadmaps = models.ManyToManyField(Roadmap)
    
    # Método decorado para indicar que es nuevo
    @property
    def is_topic_new(self):
        return (timezone.now() - self.created_at).days < 7

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
        return "User: " + str(self.user.id) + " | " + "Course: " + str(self.roadmap.id)
    
class UnitMembership(models.Model):

    """Creamos ésta clase, porque no le queremos delegar ésta tabla a Python así le podemos agregar nosotros los campos created_at y updated_at para saber el
    orden cronológico en el que el usuario se enlistó a sus cursos"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False) # Si checkeamos la box o no
    created_at = models.DateTimeField(auto_now_add=True) # Cuando se creó la membresía (fila de ésta tabla)
    updated_at = models.DateTimeField(auto_now=True) # Cuando se modíficó la membresía

    def __str__(self):
        return "User: " + str(self.user.id) + " | " + "Course: " + str(self.unit.id)

class ItemMembership(models.Model):

    """Creamos ésta clase, porque no le queremos delegar ésta tabla a Python así le podemos agregar nosotros los campos created_at y updated_at para saber el
    orden cronológico en el que el usuario se enlistó a sus cursos"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False) # Si checkeamos la box o no
    created_at = models.DateTimeField(auto_now_add=True) # Cuando se creó la membresía (fila de ésta tabla)
    updated_at = models.DateTimeField(auto_now=True) # Cuando se modíficó la membresía

    def __str__(self):
        return "User: " + str(self.user.id) + " | " + "Course: " + str(self.item.id)