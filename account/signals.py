from django.db.models.signals import post_save
from account.models import Account, Profile, SocialNetwork, History, ContentType
from django.dispatch import receiver, Signal

#Definimos el reciever que creará un profile y lo conectará a la instancia que llama a ésta signal
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
#Conectamos al reciever de arriba con el momento en que se guarde una instancia de Account
post_save.connect(create_profile, sender=Account)

#Definimos el reciever que guardará la instancia de profile
def update_profile(sender, instance, created, *args, **kwargs):
    if created == False:
        instance.profile.save()
#Conectamos el reciever de arriba con el sender cuando se actualice una instancia de Account
post_save.connect(update_profile, sender=Account)

#Creamos el reciever que se ejecutará cuando se crée un profile
def create_sn_obj(sender, instance, created, *args, **kwargs):
    if created:
        sn = SocialNetwork.objects.create()
        Profile.objects.filter(pk=instance.pk).update(social_networks=sn)
#Conectamos el reciever de arriba con el momento en que se crée un Profile
post_save.connect(create_sn_obj, sender=Profile)

#Acá declaramos la signal que va a crear un ítem en nuestro historial
object_viewed_signal = Signal(providing_args=['instance', 'request'])

#Creamos el reciever para ls ginal object_viewed_signal
def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    new_history = History.objects.create(
        account = request.user,
        content_type = ContentType.objects.get_for_model(sender),
        object_id = instance.id,
    )

object_viewed_signal.connect(object_viewed_receiver)