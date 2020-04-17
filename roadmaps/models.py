from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Topic(models.Model):
    title = models.CharField(
        null=False,
        max_length=30,
        validators=[MinLengthValidator(2, 'Title must be greater tahn 2 characters')]
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
    completed_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='finished_roadmaps',
        blank=True,
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
    
    topics = models.ManyToManyField(Topic)
    
    methods_and_resources = models.CharField(max_length=250, default='')

    estimated_time = models.CharField(max_length=100, default='')

    # Campo de miembros para ver quien es miembro de un roadmap y quien no
    # members = models.ManyToManyField(
    #     settings.AUTH_USER_MODEL, # Modelo con el que matchea éste campo
    #     through='Membership', # Indicamos qué modelo de éste documente será la joint table
    #     related_name='roadmaps', # Nombre delquery de éste campo en la joint table
    # )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
# Tabla Joint de Miembros    
# class Membership(models.Model):

#     """Creamos ésta clase, porque no le queremos delegar ésta tabla a Python así le podemos agregar nosotros los campos created_at y updated_at para saber el
#     orden cronológico en el que el usuario se enlistó a sus cursos"""

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return "User: " + str(self.user.id) + " | " + "Course: " + str(self.roadmap.id)


class Unit(models.Model):
    completed_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='finished_units'
    )
    name = models.CharField(
        null=False,
        max_length=30,
        validators=[MinLengthValidator(2, 'Title must be greater than 2 characters')]
    )
    # Campo para indicar el orden
    place = models.IntegerField(null=False, default=1)
    about = models.TextField()
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE)

    def __str__(self):
        return "Unit " + str(self.place) +": " + self.name
    

class Item(models.Model):
    completed_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='finished_items'
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
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return self.title